import os
import subprocess
from tempfile import mkstemp
from pathlib import Path

import click
from pandas import read_csv, DataFrame, set_option  # type: ignore

# Avoid pandas truncation of the commands description
set_option("display.max_colwidth", -1)


def convert_dataframe(dataframe: DataFrame, output: Path) -> None:
    """Convert a pandas DataFrame to another table format"""
    file_format = output.suffix[1:]
    try:
        # Create temporary file to store HTML table
        tempf, temporary_file = mkstemp(text=True)
        with open(tempf, "w") as tf:
            dataframe.to_html(buf=tf, index=False)
        # Use pandoc to convert from HTML to DOCX
        cmd = f"pandoc --from=html --to={file_format} -o {output} {temporary_file}"
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    finally:
        # Remove temp file
        os.remove(temporary_file)

    print(f"{output} created.")


def select_and_convert(df: DataFrame, csv_file: Path, ext: str, cmd_type=None) -> None:
    if cmd_type is not None:
        df = df.query(f"type == '{cmd_type.upper()}'")
        df = df.drop(columns="type")
    suffix = f".{ext}" if cmd_type is None else f"_{cmd_type}.{ext}"
    output = csv_file.with_name(csv_file.stem + suffix)
    convert_dataframe(df, output)


@click.command("convert")
@click.argument("csv_file", type=click.Path(exists=True))
@click.option(
    "--to",
    "extension",
    type=str,
    default="docx",
    show_default=True,
    help="Output file extension.",
)
@click.option("--sort", is_flag=True, help="Orders commands alphabetically.")
@click.option("--split", is_flag=True, help="Splits the output into actions and queries.")
def main(csv_file, extension, split, sort):
    input_file = Path(csv_file)

    commands: DataFrame = read_csv(input_file)

    commands.replace("NORMAL", "NORM", inplace=True)
    commands.replace("ENGINEERING1", "ENG1", inplace=True)
    commands.replace("ENGINEERING2", "ENG2", inplace=True)
    commands.replace("ENGINEERING3", "ENG3", inplace=True)

    if sort:
        commands.sort_values("class", inplace=True)

    if split:
        select_and_convert(commands, input_file, extension, cmd_type='action')
        select_and_convert(commands, input_file, extension, cmd_type='query')
    else:
        select_and_convert(commands, input_file, extension)
