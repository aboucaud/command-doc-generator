from functools import namedtuple


COMMAND_ARGS = [
    "type",
    "level",
    "alias",
    "description",
]

CSV_HEADER = "class,name,type,level,description\n"

class Command:
    def __init__(self, name, cmdtype, level, description):
        self.name = name
        self.type = clean_type(cmdtype)
        self.level = clean_level(level)
        self.description = clean_description(description)

    def __repr__(self):
        return f"{self.name}: {self.description}"

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"name={self.name}, "
            f"type={self.type}, "
            f"level={self.level}, "
            f"desc={self.description})"
        )

    def to_csv(self, java_class_name):
        return (
            f"{java_class_name},"
            f"{self.name},"
            f"{self.type},"
            f"{self.level},"
            f"{self.description}"
            "\n"
        )


def is_correct_entry(text):
    for arg in COMMAND_ARGS:
        if text.strip().startswith(arg):
            return True
    else:
        return False

def clean_level(text):
    return text.replace('Command.', '')

def clean_type(text):
    return text.replace('Command.CommandType.', '')

def clean_description(text):
    if text.startswith('"'):
        text = text[1:]
    if text.endswith('"'):
        text = text[:-1]

    text = text.replace('" + "', '')
    text = text.replace('"+ "', '')
    text = text.replace('" +"', '')
    return text.capitalize()
