from ccsdoc.command import Command
from ccsdoc.command import is_correct_entry


def parse_file(filepath):
    text = filepath.read_text()

    lines = split_and_remove_whitespace(text)

    command_idx = get_command_position(lines)

    commands = []
    for idx in command_idx:
        try:
            command = extract_command_info(lines, idx)
            commands.append(command)
        except Exception as e:
            print(f"=> {filepath}: issue at line {idx}: {e}")

    return commands


def split_and_remove_whitespace(text):
    return [
        line.strip()
        for line in text.split("\n")
    ]


def get_command_position(lines):
    return [
        idx
        for idx, line in enumerate(lines)
        if line.startswith("@Command")
    ]


def extract_command_name(line):
    # Use the method call to break the string
    before_call = line.split('(')[0]
    # The remaining text should end with the method_name
    *_, method_name = before_call.split()

    return method_name


def extract_command_arguments(decorator):
    # Remove the @Command(...)
    content = decorator[9:-1]

    # Separate arguments
    entries = content.split(",")

    # Use '=' as an indicator of the number of arguments
    # (will fail if '=' present in the command description)
    n_entries = content.count('=')
    n_splits = content.count(",")

    if n_splits >= n_entries:
        new_entries = []
        for entry in entries:
            if is_correct_entry(entry):
                new_entries.append(entry)
            else:
                new_entries[-1] += entry
        entries = new_entries

    # Extract the arguments in a dictionary
    args = {}
    for entry in entries:
        arg, value = entry.split('=')
        args[arg.strip()] = value.strip()

    for key in ["type", "level", "description"]:
        if key not in list(args.keys()):
            raise ValueError(f"Missing command argument '{key}'.")

    return args


def extract_command_info(lines, idx):
    # Command decorator
    cmd = lines[idx]
    while not cmd.endswith(')'):
        idx += 1
        cmd += lines[idx]

    command_dict = extract_command_arguments(cmd)

    # Method definition
    method_id = idx + 1
    method = lines[method_id]
    while method.startswith('@Override') or method.startswith('//'):
        method_id += 1
        method = lines[method_id]

    command_name = extract_command_name(method)

    return Command(
        name=command_name,
        cmdtype=command_dict['type'],
        level=command_dict['level'],
        description=command_dict['description'],
    )
