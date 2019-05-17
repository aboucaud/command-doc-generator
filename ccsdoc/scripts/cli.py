import click
import pathlib

from ccsdoc.parser import parse_file
from ccsdoc.command import Command, CSV_HEADER

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


def process_commands(filepath, output=None):
    commands = parse_file(filepath)
    if commands:
        if output is None:
            print_file_commands(filepath.name, commands)
        else:
            save_file_commands(filepath.name, commands, output)


def print_file_commands(filename, commands):
    print(f"{color.BOLD}{filename}:{color.END}")
    for command in commands:
        print(command)
    print("")


def save_file_commands(filename, commands, output):
    with output.open('a') as f:
        for command in commands:
            f.write(command.to_csv(filename))


@click.command()
@click.argument(
    "path",
    type=click.Path(exists=True)
)
@click.option(
    "-o", "--output",
    type=click.Path(dir_okay=False),
    default=None
)
def cli(path, output):
    path = pathlib.Path(path)

    if output is not None:
        output = pathlib.Path(output)
        if output.exists():
            import sys
            sys.exit("Output file already exists, cancelling action.")
        output.write_text(CSV_HEADER)

    if not path.is_dir():
        process_commands(path, output)
    else:
        # Look for all .java files
        targets = list(path.rglob("*.java"))

        # Do not consider the test files
        targets = filter(lambda x: "test" not in str(x.parent), targets)

        # Do not consider simulation files
        targets = filter(lambda x: "Simu" not in str(x.name), targets)

        # Do not consider package-info.java files
        targets = filter(lambda x: x.name != "package-info.java", targets)

        for filepath in targets:
            process_commands(filepath, output)
