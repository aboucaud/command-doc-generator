from typing import Optional

from ccsdoc.text import clean_description


class Argument:
    def __init__(self, name: str, ptype: str, desc: Optional[str] = None):
        self.name = name
        self.type = ptype
        self.description = clean_description(desc) if desc else ""

    def __repr__(self):
        return (
            f"{self.type} {self.name}"
        )

    def __str__(self):
        return (
            f"{self.__class__.__name__}["
            f"name={self.name}"
            f", type={self.type}"
            f"{', desc=' + self.description if self.description else ''}"
            "]"
        )
