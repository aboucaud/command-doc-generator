from enum import Enum
from typing import List, Optional, Iterator
from pathlib import Path
import click

from ccsdoc.parser import parse_file
from ccsdoc.command import Command, CSV_HEADER


class Color(Enum):
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def process_commands(filepath: Path, output: Optional[Path] = None) -> None:
    commands: List[Command] = parse_file(filepath)
    class_name = filepath.stem
    if commands:
        if output is None:
            print_file_commands(commands, class_name)
        else:
            save_file_commands(output, commands, class_name)


def print_file_commands(commands: List[Command], class_name: str) -> None:
    print(f"{Color.BOLD.value}{class_name}:{Color.END.value}")
    for command in commands:
        print(command)
    print("")


def save_file_commands(output: Path, commands: List[Command], class_name: str) -> None:
    with output.open("a") as f:
        for command in commands:
            f.write(command.to_csv(class_name))


@click.command("parse")
@click.option(
    "--path",
    type=click.Path(exists=True),
    default=".",
    show_default=True,
    help="Path to a file or directory to explore and retrieve commands from.",
)
@click.option(
    "--to",
    "output",
    type=click.Path(dir_okay=False),
    default=None,
    show_default=True,
    help="If specified, produces a CSV catalogue of the available commands.",
)
def main(path: Path, output: Path):
    path = Path(path)

    if output is not None:
        output = Path(output)
        if output.exists():
            import sys

            sys.exit("Output file already exists, cancelling action.")
        output.write_text(CSV_HEADER)

    if not path.is_dir():
        process_commands(path, output)
    else:
        # Look for all .java files
        # targets: Iterator[Path] = list(path.rglob("*.java"))
        targets: Iterator[Path] = path.rglob("*.java")

        # Do not consider the test files
        targets = filter(lambda x: "test" not in str(x.parent), targets)

        # Do not consider simulation files
        targets = filter(lambda x: "Simu" not in str(x.name), targets)

        # Do not consider package-info.java files
        targets = filter(lambda x: x.name != "package-info.java", targets)

        for filepath in targets:
            process_commands(filepath, output)
