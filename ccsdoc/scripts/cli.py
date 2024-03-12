"""
ccsdoc main command line interface

\b
select one of the following actions:
- `parse`:      create a catalogue of available commands in a given subsystem
- `convert`:    convert the command catalog to a given extension
                needs the conversion tool `pandoc` installed
- `trending`:   create a catalogue of trending values for the subsystem

"""
import click

from ccsdoc.scripts import parse
from ccsdoc.scripts import convert
from ccsdoc.scripts import trending


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, help=__doc__)
def cli():
    pass


cli.add_command(parse.main)
cli.add_command(convert.main)
cli.add_command(trending.main)
