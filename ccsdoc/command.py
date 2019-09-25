from typing import List, Dict

COMMAND_ARGS: List[str] = ["type", "level", "alias", "description"]
MANDATORY_COMMAND_ARGS: List[str] = ["type", "level", "description"]


COMMAND_HEADER: str = "class,name,type,level,description\n"


class Command:
    def __init__(self, name: str, cmdtype: str, level: str, description: str) -> None:
        self.name = name
        self.type = clean_type(cmdtype)
        self.level = clean_level(level)
        self.description = clean_description(description)

    def __repr__(self) -> str:
        return f"{self.name}: {self.description}"

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"type={self.type}, "
            f"level={self.level}, "
            f"desc={self.description})"
        )

    def to_csv(self, class_name: str) -> str:
        return (
            f"{class_name},"
            f"{self.name},"
            f"{self.type},"
            f"{self.level},"
            f"{self.description}"
            "\n"
        )


def is_command(line: str) -> bool:
    return line.startswith("@Command")


def is_correct_command_entry(text: str) -> bool:
    for arg in COMMAND_ARGS:
        if text.strip().startswith(arg):
            return True
    else:
        return False


def clean_level(text: str) -> str:
    return text.replace("Command.", "")


def clean_type(text: str) -> str:
    return text.replace("Command.CommandType.", "")


def clean_description(text: str) -> str:
    if text.startswith('"'):
        text = text[1:]
    if text.endswith('"'):
        text = text[:-1]

    text = text.replace('" + "', "")
    text = text.replace('"+ "', "")
    text = text.replace('" +"', "")
    return text.capitalize()


def extract_command_name(line: str) -> str:
    # Use the method call to break the string
    before_call = line.split("(")[0]
    # The remaining text should end with the method_name
    *_, method_name = before_call.split()

    return method_name


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
