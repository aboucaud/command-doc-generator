from typing import List

COMMAND_ARGS: List[str] = ["type", "level", "alias", "description"]

CSV_HEADER: str = "class,name,type,level,description\n"


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


def is_correct_entry(text: str) -> bool:
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
