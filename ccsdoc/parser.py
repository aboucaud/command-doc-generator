from typing import List, Tuple
from pathlib import Path

from ccsdoc.command import Command
from ccsdoc.argument import Argument
from ccsdoc.parameter import ConfigParameter
from ccsdoc.parameter import is_config_parameter
from ccsdoc.parameter import extract_parameter_name
from ccsdoc.parameter import extract_parameter_arguments


def parse_file(filepath: Path) -> Tuple[List[Command], List[ConfigParameter]]:
    text = filepath.read_text()

    lines = split_and_remove_whitespace(text)

    commands = []
    for idx in get_command_position(lines):
        try:
            command = extract_command_info(lines, idx)
            commands.append(command)
        except Exception as e:
            print(f"=> {filepath}: issue at line {idx}: {e}")

    params = []
    for idx in get_param_position(lines):
        try:
            parameter = extract_param_info(lines, idx)
            if parameter.deprecated:
                continue
            params.append(parameter)
        except Exception as e:
            print(f"=> {filepath}: issue at line {idx}: {e}")

    return commands, params


def split_and_remove_whitespace(text: str) -> List[str]:
    return [line.strip() for line in text.split("\n")]


def get_command_position(lines: List[str]) -> List[int]:
    return [idx for idx, line in enumerate(lines) if is_command(line)]


def get_param_position(lines: List[str]) -> List[int]:
    return [idx for idx, line in enumerate(lines) if is_config_parameter(line)]


def extract_command_info(lines: List[str], idx: int) -> Command:
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
        cmdtype=command_dict.get("type", ""),
        level=command_dict.get("level", ""),
        description=command_dict.get("description", ""),
        args=arguments,
    )


def extract_param_info(lines: List[str], idx: int) -> ConfigParameter:
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

    definition = lines[idx + 1]
    param_name = extract_parameter_name(definition)

    return ConfigParameter(
        name=param_name,
        description=param_dict.get("description", " "),
        deprecated=deprecated,
    )
