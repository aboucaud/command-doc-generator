from typing import List, Optional, Iterator
from pathlib import Path
import click

from ccsdoc.parameter import DataAttribute
from ccsdoc.parser import parse_trending_params
from ccsdoc.scripts.parse import Color


def process_trending(filepath: Path, output: Optional[Path] = None):
    parameters = parse_trending_params(filepath.read_text(), filepath.name)
    class_name = filepath.stem.replace("StatusDataPublishedBy", "")
    if output is None:
        print(f"\n{Color.BOLD.value}{class_name}:{Color.END.value} {filepath.as_posix()}\n")
        for param in parameters:
            print(param)
        print("")
    else:
        tmy_out = output.joinpath(output.name + "_tmy.csv")
        save_to_file(tmy_out, parameters, class_name)


def save_to_file(output: Path, infos: List[DataAttribute], class_name: str) -> None:
    with output.open("a") as f:
        for info in infos:
            # Do not write the parameters only used for GUI
            if not info.skip:
                f.write(info.to_csv(class_name))


@click.command("trending")
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
    help="If specified, produces a CSV catalogue of the available telemetry parameters.",
)
def main(path: Path, output: Path) -> None:
    path = Path(path)

    if output is not None:
        output = Path(output)
        if output.exists():
            import sys
            sys.exit("Output dir already exists, cancelling action.")

        output.mkdir()

    if not path.is_dir():
        if path.stem.startswith("StatusDataPublishedBy"):
            process_trending(path, output)
        else:
            print("")
    else:
        # Look for all telemetry files
        targets: Iterator[Path] = path.rglob("StatusDataPublishedBy*.java")

        # Do not consider the test files
        targets = filter(lambda x: "test" not in str(x.parent), targets)

        # Do not consider simulation files
        targets = filter(lambda x: "Simu" not in str(x.name), targets)

        for filepath in targets:
            process_trending(filepath, output)
