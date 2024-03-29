from enum import Enum
from typing import List, Optional, Iterator, Union
from pathlib import Path
import click

from ccsdoc.parser import parse_raw_text
from ccsdoc.command import Command, COMMAND_HEADER
from ccsdoc.parameter import ConfigurationParameter, PARAM_HEADER


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


def process_commands(filepath: Path, output: Optional[Path] = None, commands_only: bool = False, params_only: bool = False) -> None:
    commands, parameters = parse_raw_text(filepath.read_text(), filepath.name)
    class_name = filepath.stem
    if commands and not params_only:
        if output is None:
            print(f"\n{Color.BOLD.value}{class_name}:{Color.END.value} {filepath.as_posix()}\n")
            for command in commands:
                print(command)
            print("")
        else:
            cmd_out = output.joinpath(output.name + "_cmd.csv")
            save_to_file(cmd_out, commands, class_name)
    if parameters and not commands_only:
        if output is None:
            print(f"\n{Color.BOLD.value}{class_name}:{Color.END.value} {filepath.as_posix()}\n")
            for param in parameters:
                print(param)
            print("")
        else:
            param_out = output.joinpath(output.name + "_param.csv")
            save_to_file(param_out, parameters, class_name)


def save_to_file(output: Path, infos: Union[List[Command], List[ConfigurationParameter]], class_name: str) -> None:
    with output.open("a") as f:
        for info in infos:
            f.write(info.to_csv(class_name))


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
    type=click.Path(dir_okay=True),
    default=None,
    show_default=True,
    help="If specified, produces a CSV catalogue of the available commands.",
)
@click.option(
    "--commands",
    "commands_only",
    type=click.BOOL,
    is_flag=True,
    help="If given, only prints commands info"
)
@click.option(
    "--params",
    "params_only",
    type=click.BOOL,
    is_flag=True,
    help="If given, only prints configuration parameters info"
)
def main(path: Path, output: Path, commands_only: bool, params_only: bool):
    path = Path(path)

    if output is not None:
        output = Path(output)
        if output.exists():
            import sys
            sys.exit("Output dir already exists, cancelling action.")

        output.mkdir()

        if not params_only:
            cmd_out = output.joinpath(output.name + "_cmd.csv")
            cmd_out.write_text(COMMAND_HEADER)
        if not commands_only:
            param_out = output.joinpath(output.name + "_param.csv")
            param_out.write_text(PARAM_HEADER)

    if not path.is_dir():
        process_commands(path, output, commands_only, params_only)
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
            process_commands(filepath, output, commands_only, params_only)
