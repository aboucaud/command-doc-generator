from ccsdoc.command import clean_description

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
            f"{self.__class__.__name__}["
            f"name={self.name}, "
            f"desc='{self.description}'"
            "]"
        )

    def to_csv(self, class_name: str) -> str:
        return (
            f"{class_name},"
            f"{self.name},"
            f"{self.description}"
            "\n"
        )
