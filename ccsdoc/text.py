from typing import Dict, List, Tuple, Optional

COMMAND_ARGS: List[str] = ["type", "level", "alias", "description", "autoAck", "timeout"]
MANDATORY_COMMAND_ARGS: List[str] = ["type", "level", "description"]
PARAM_ARGS: List[str] = ["description", "range", "units", "category", "is_final"]
DATA_ATTRIBUTE_ARGS: List[str] = ["description", "units"]


def is_command(line: str) -> bool:
    """Does the line refer to a command"""
    return line.startswith("@Command")


def is_correct_command_entry(text: str) -> bool:
    """Is the keyword a valid command argument"""
    for arg in COMMAND_ARGS:
        if text.strip().startswith(arg):
            return True

    return False


def clean_command_level(text: str) -> str:
    """Remove parents from the command level"""
    return text.replace("Command.", "")


def clean_command_type(text: str) -> str:
    """Remove parents from the command type"""
    text = text.replace("Command.", "")
    text = text.replace("CommandType.", "")

    return text


def clean_quotes(text: str) -> str:
    """Remove quotes from string"""
    if text.startswith('"'):
        text = text[1:]
    if text.endswith('"'):
        text = text[:-1]

    return text


def clean_description(text: str) -> str:
    """Format description to linearize it from multiline definition"""
    text = clean_quotes(text)

    text = text.replace('" + "', "")
    text = text.replace('"+ "', "")
    text = text.replace('" +"', "")

    sentences = text.split(".")
    description = ". ".join([sentence.strip().capitalize() for sentence in sentences])
    description = description.strip()

    return description


def extract_command_name(line: str) -> str:
    """Read command name from text"""
    # Use the method call to break the string
    before_call = line.split("(")[0]
    # The remaining text should end with the method_name
    *_, method_name = before_call.split()

    return method_name


def extract_method_arguments(line: str) -> Dict[str, str]:
    """Read method arguments from text"""
    # Use the method call to break the string
    arguments_str = line.split("(")[1].split(")")[0]

    if not arguments_str:
        return {}

    args = {}
    for entry in arguments_str.split(","):
        type_, argname = entry.strip().split()
        args[argname.strip()] = type_.strip()

    return args


def extract_command_arguments(decorator: str) -> Dict[str, str]:
    """Read command arguments from text"""
    # Remove the @Command(...)
    content = decorator[9:-1]

    # Separate arguments
    entries = content.split(",")

    # Use '=' as an indicator of the number of arguments
    # (will fail if '=' present in the command description)
    n_entries = content.count("=")
    n_splits = content.count(",")

    if n_splits >= n_entries:
        new_entries = []
        for entry in entries:
            if is_correct_command_entry(entry):
                new_entries.append(entry)
            else:
                new_entries[-1] += entry
        entries = new_entries

    # Extract the arguments in a dictionary
    args = {}
    for entry in entries:
        arg, value = entry.split("=")
        args[arg.strip()] = value.strip()

    for key in MANDATORY_COMMAND_ARGS:
        if key not in list(args):
            raise ValueError(f"Missing command argument '{key}'.")

    return args


def is_correct_parameter_entry(text: str) -> bool:
    """Is the keyword a valid configuration parameter argument"""
    for arg in PARAM_ARGS:
        if text.strip().startswith(arg):
            return True

    return False


def is_config_parameter(line: str) -> bool:
    """Does the line refer to a configuration parameter"""
    return line.startswith("@ConfigurationParameter") and not line.endswith("Changer")


def extract_parameter_name_and_type(line: str) -> Tuple[str, str]:
    """Read configuration parameter name from text"""
    # Remove default value if any
    line, *_ = line.split("=")
    line = line.strip()

    # Parameter is now the last entry of the line
    *_, type_, param_name = line.strip().split()
    # Remove the final ;
    if param_name.endswith(";"):
        param_name = param_name[:-1]

    return param_name, type_


def extract_parameter_arguments(decorator: str) -> Dict[str, str]:
    """Read configuration parameter arguments from text"""
    # Remove the @ConfigurationParameter(...)
    left = decorator.index("(")
    content = decorator[left + 1:-1]

    # Separate arguments
    entries = content.split(",")

    # Use '=' as an indicator of the number of arguments
    # (will fail if '=' present in the command description)
    n_entries = content.count("=")
    n_splits = content.count(",")

    if n_splits >= n_entries:
        new_entries = []
        for entry in entries:
            if is_correct_parameter_entry(entry):
                new_entries.append(entry)
            else:
                new_entries[-1] += entry
        entries = new_entries

    # Extract the arguments in a dictionary
    args = {}
    for entry in entries:
        arg, value = entry.split("=")
        args[arg.strip()] = value.strip()

    return args


def extract_range_values(range_string: str) -> Tuple[Optional[int], Optional[int]]:
    """Extract the authorized range of values from parameter definition"""
    low_val = None
    high_val = None

    values = range_string.strip('"').split('..')

    try:
        low_val = int(values[0])
    except ValueError:
        pass

    try:
        high_val = int(values[1])
    except ValueError:
        pass

    return (low_val, high_val)


def is_data_attribute(line: str) -> bool:
    """Does the line refer to a data attribute"""
    return line.startswith("@DataAttributes")


def is_correct_data_attribute_entry(text: str) -> bool:
    """Is the keyword a valid command data attribute"""
    for arg in DATA_ATTRIBUTE_ARGS:
        if text.strip().startswith(arg):
            return True

    return False


def is_only_for_gui(line: str) -> bool:
    """Is the value only used for the GUI"""
    return line.startswith("@SkipEncoding") or line.startswith("@DoNotTrend")
