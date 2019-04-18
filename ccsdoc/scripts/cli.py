import click
import pathlib

from ccsdoc.parser import parse_file
from ccsdoc.command import Command

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def print_file_commands(filepath):
    print(f"{color.BOLD}{filepath.name}:{color.END}")

    commands = parse_file(filepath)
    if commands:
        for command in commands:
            print(command)
    else:
        print(f"=> no commands")


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True)
)
def cli(path):
    path = pathlib.Path(path)
    if not path.is_dir():
        print_file_commands(path)
    else:
        # Look for all .java files
        targets = list(path.rglob("*.java"))

        # Do not consider the test files
        targets = filter(lambda x: "test" not in str(x.parent), targets)

        # Do not consider package-info.java files
        targets = filter(lambda x: x.name != "package-info.java", targets)

        for filepath in targets:
            print_file_commands(filepath)
            print("")
