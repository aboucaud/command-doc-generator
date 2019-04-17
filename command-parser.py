from functools import namedtuple
from textwrap import dedent
from argparse import ArgumentParser

import numpy as np


Command = namedtuple('Command', ['name', 'type', 'level', 'description'])


def parse_args():
    parser = ArgumentParser(
        description="Parse a subsystem Java directory to list commands"
    )
    parser.add_argument("path", type=str, help="path to the Java directory")

    return parser.parse_args()


def parse_file(filename):
    with open(filename, 'r') as f:
        text = dedent(f.read())

    lines = [
        line.strip()
        for line in text.split("\n")
    ]

    line_number = np.arange(len(lines))
    command_lines = [
        line.startswith("@Command")
        for line in lines
    ]
    command_idx = line_number[command_lines]

    commands = []
    cmd_name = []
    for idx in command_idx:
        current_id = idx
        commandline = lines[idx]
        while not commandline.endswith(")"):
            current_id += 1
            commandline += lines[current_id]
        commands.append(commandline)
        name_id = current_id + 1
        name_line = lines[name_id]
        if name_line.startswith('@'):
            name_line = lines[name_id + 1]
        cmd_name.append(name_line)

    return cmd_name, commands


def read_name(name_line):
    before_call = name_line.split('(')[0]
    name = before_call.split()[-1]
    return name


def read_command(name, command_line):
    content = command_line[9:-1]
    entries = content.split(",")
    args = {}
    for entry in entries:
        arg, value = entry.split('=')
        args[arg.strip()] = value.strip()

    return Command(
        name=name,
        type=args['type'],
        level=args['level'],
        description=args['description'][1:-1]
    )
    # return Command(type=cmdtype, level=lvl, description=desc)


def main():
    args = parse_args()

    name_lines, command_lines = parse_file(args.path)

    for name_line, cmd in zip(name_lines, command_lines):
        try:
            name = read_name(name_line)
            command = read_command(name, cmd)
            print(command)
        except ValueError as e:
            print()
            print(e)
            print(cmd)
            print()


if __name__ == "__main__":
    main()
