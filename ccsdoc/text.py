from typing import Dict, List

COMMAND_ARGS: List[str] = ["type", "level", "alias", "description", "autoAck", "timeout"]
MANDATORY_COMMAND_ARGS: List[str] = ["type", "level", "description"]
PARAM_ARGS: List[str] = ["description", "range", "category", "is_final"]


def is_command(line: str) -> bool:
    return line.startswith("@Command")


def is_correct_command_entry(text: str) -> bool:
    for arg in COMMAND_ARGS:
        if text.strip().startswith(arg):
            return True
    else:
        return False


def clean_command_level(text: str) -> str:
    return text.replace("Command.", "")


def clean_command_type(text: str) -> str:
    text = text.replace("Command.", "")
    text = text.replace("CommandType.", "")

    return text


def clean_description(text: str) -> str:
    if text.startswith('"'):
        text = text[1:]
    if text.endswith('"'):
        text = text[:-1]

    text = text.replace('" + "', "")
    text = text.replace('"+ "', "")
    text = text.replace('" +"', "")

    sentences = text.split(".")
    description = ". ".join([sentence.strip().capitalize() for sentence in sentences])
    description = description.strip()

    return description


def extract_command_name(line: str) -> str:
    # Use the method call to break the string
    before_call = line.split("(")[0]
    # The remaining text should end with the method_name
    *_, method_name = before_call.split()

    return method_name


def extract_method_arguments(line: str) -> Dict[str, str]:
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
        if key not in list(args.keys()):
            raise ValueError(f"Missing command argument '{key}'.")

    return args


def is_correct_parameter_entry(text: str) -> bool:
    for arg in PARAM_ARGS:
        if text.strip().startswith(arg):
            return True
    else:
        return False


def is_config_parameter(line: str) -> bool:
    return line.startswith("@ConfigurationParameter") and not line.endswith("Changer")


def extract_parameter_name(line: str) -> str:
    # Remove default value if any
    line, *_ = line.split("=")
    # Parameter is now the last entry of the line
    *_, parameter = line.strip().split(" ")
    # Remove the final ;
    if parameter.endswith(";"):
        parameter = parameter[:-1]

    return parameter


def extract_parameter_arguments(decorator: str) -> Dict[str, str]:
    # Remove the @ConfigurationParameter(...)
    content = decorator[24:-1]

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
