from typing import List, Tuple, Optional

from ccsdoc.command import Command
from ccsdoc.parameter import Argument
from ccsdoc.parameter import ConfigurationParameter
from ccsdoc.parameter import DataAttribute
from ccsdoc.text import is_command
from ccsdoc.text import is_config_parameter
from ccsdoc.text import is_data_attribute
from ccsdoc.text import is_only_for_gui
from ccsdoc.text import extract_command_name
from ccsdoc.text import extract_command_arguments
from ccsdoc.text import extract_method_arguments
from ccsdoc.text import extract_parameter_name_and_type
from ccsdoc.text import extract_parameter_arguments
from ccsdoc.text import extract_range_values


def parse_raw_text(
        raw_text: str,
        filename: Optional[str] = None
) -> Tuple[List[Command], List[ConfigurationParameter]]:
    """Parse text directly from Java file"""
    lines = split_and_remove_whitespace(raw_text)

    commands = []
    for idx in get_command_position(lines):
        try:
            command = extract_command_info(lines, idx)
            commands.append(command)
        except ValueError as exception:
            print(
                f"=> {filename + ': ' if filename else ''}"
                f"command issue at line {idx}: {exception}"
            )

    params = []
    for idx in get_param_position(lines):
        try:
            parameter = extract_param_info(lines, idx)
            if parameter.deprecated:
                continue
            params.append(parameter)
        except ValueError as exception:
            print(
                f"=> {filename + ': ' if filename else ''}",
                f"config parameter issue at line {idx}: {exception}"
            )

    return commands, params


def split_and_remove_whitespace(text: str) -> List[str]:
    """Convert raw text to list of line strings"""
    return [line.strip() for line in text.split("\n")]


def get_command_position(lines: List[str]) -> List[int]:
    """Get line numbers of @Commands"""
    return [idx for idx, line in enumerate(lines) if is_command(line)]


def get_param_position(lines: List[str]) -> List[int]:
    """Get line numbers of @ConfigurationParameters"""
    return [idx for idx, line in enumerate(lines) if is_config_parameter(line)]


def extract_command_info(lines: List[str], idx: int) -> Command:
    """Create a Command instance from text"""
    # Command decorator
    cmd_decorator = lines[idx]
    while not cmd_decorator.endswith(")"):
        idx += 1
        cmd_decorator += lines[idx]

    command_dict = extract_command_arguments(cmd_decorator)

    # Method definition
    method_id = idx + 1
    method = lines[method_id]
    while method.startswith("@Override") or method.startswith("//"):
        method_id += 1
        method = lines[method_id]

    command_name = extract_command_name(method)
    argument_dict = extract_method_arguments(method)
    arguments = [
        Argument(name, type_)
        for name, type_ in argument_dict.items()
    ]

    return Command(
        name=command_name,
        cmd_type=command_dict.get("type", ""),
        level=command_dict.get("level", ""),
        description=command_dict.get("description", ""),
        args=arguments,
    )


def extract_param_info(lines: List[str], idx: int) -> ConfigurationParameter:
    """Create a ConfigurationParameter instance from text"""
    # Verify if the parameter is deprecated
    deprecated = "@Deprecated" in lines[idx - 1]

    param_decorator = lines[idx]
    if "(" in param_decorator:
        while not param_decorator.endswith(")"):
            idx += 1
            param_decorator += lines[idx]

        param_dict = extract_parameter_arguments(param_decorator)
    else:
        param_dict = {}

    low_val, high_val = extract_range_values(param_dict.get("range", ".."))

    definition = lines[idx + 1]
    param_name, ptype = extract_parameter_name_and_type(definition)

    return ConfigurationParameter(
        name=param_name,
        category=param_dict.get("category", "UNKNOWN"),
        ptype=ptype,
        units=param_dict.get("units", None),
        low=low_val,
        high=high_val,
        description=param_dict.get("description", None),
        is_deprecated=deprecated,
    )


def get_data_attribute_position(lines: List[str]) -> List[int]:
    """Get line numbers of published telemetry parameters"""
    return [
        idx for idx, line in enumerate(lines)
        if is_data_attribute(line)
    ]


def extract_trending_info(lines: List[str], idx: int) -> DataAttribute:
    """Create a DataAttribute instance from text"""
    param_decorator = lines[idx]
    skip = False

    if not "(" in param_decorator:
        raise ValueError("Missing description for DataAttribute")

    while not param_decorator.endswith(")"):
        idx += 1
        param_decorator += lines[idx]

    param_dict = extract_parameter_arguments(param_decorator)
    definition = lines[idx + 1]
    if is_only_for_gui(lines[idx - 1]):
        skip = True
    elif is_only_for_gui(lines[idx + 1]):
        skip = True
        definition = lines[idx + 2]
    param_name, ptype = extract_parameter_name_and_type(definition)
    param = DataAttribute(
        name=param_name,
        ptype=ptype,
        description=param_dict.get("description", None),
        units=param_dict.get("units", None),
        skip=skip
    )

    return param


def parse_trending_params(raw_text: str, filename: Optional[str] = None) -> List[DataAttribute]:
    """Parse telemetry params directly from Java file"""
    lines = split_and_remove_whitespace(raw_text)

    params = []
    for idx in get_data_attribute_position(lines):
        try:
            parameter = extract_trending_info(lines, idx)
            params.append(parameter)
        except ValueError as exception:
            print(
                f"=> {filename + ': ' if filename else ''}",
                f"trending parameter issue at line {idx}: {exception}"
            )
            raise exception

    return params
