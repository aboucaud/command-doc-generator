from typing import Dict, List

from ccsdoc.command import clean_description

PARAM_ARGS: List[str] = ["description", "range", "category", "is_final"]

PARAM_HEADER: str = "class,name,description\n"


class ConfigParameter:
    def __init__(self, name: str, description: str, deprecated: bool = False) -> None:
        self.name = name
        self.description = clean_description(description)
        self.deprecated = deprecated

    def __repr__(self) -> str:
        return f"{self.name}: {self.description}"

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"desc={self.description})"
        )

    def to_csv(self, class_name: str) -> str:
        return f"{class_name}," f"{self.name}," f"{self.description}" "\n"


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
