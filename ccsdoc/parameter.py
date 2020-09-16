from typing import Optional

from ccsdoc.text import clean_description

PARAM_HEADER: str = "class,name,type,description\n"
CONFIG_PARAM_HEADER: str = "class,name,type,low,high,description\n"


class Parameter:
    def __init__(self, name: str, ptype: str, description: Optional[str] = None) -> None:
        self.name = name
        self.type = ptype
        self.description = clean_description(description) if description else ""

    def __repr__(self) -> str:
        return (
            f"{self.type} {self.name}"
            f"{': ' + self.description if self.description else ''}"
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}["
            f"name={self.name}, "
            f"type={self.type}"
            f"""{", desc='" + self.description + "'" if self.description else ""}"""
            "]"
        )

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def to_csv(self, class_name: str) -> str:
        return (
            f"{class_name},"
            f"{self.name},"
            f"{self.type},"
            f"{self.description}"
            "\n"
        )


class ConfigurationParameter(Parameter):
    def __init__(self, name: str, ptype: str, low: Optional[int] = None, high: Optional[int] = None, description: Optional[str] = None, is_deprecated: bool = False) -> None:
        Parameter.__init__(self, name, ptype, description)
        self.low = str(low) if low is not None else "UNDEFINED"
        self.high = str(high) if high is not None else "UNDEFINED"
        self.deprecated = is_deprecated

    def __str__(self) -> str:
        text = super().__str__()
        text = text.replace("]", f", range=[{self.low}, {self.high}]]")

        if self.deprecated:
            text += "(DEPRECATED)"

        return text

    def to_csv(self, class_name: str) -> str:
        return (
            f"{class_name},"
            f"{self.name},"
            f"{self.type},"
            f"{self.low},"
            f"{self.high},"
            f"{self.description}"
            "\n"
        )


class Argument(Parameter):
    def __init__(self, name: str, ptype: str) -> None:
        Parameter.__init__(self, name, ptype, description=None)
