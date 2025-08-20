import curses
import pyperclip
def interactive_mode(commands_file, remove_mode=False):
    commands = load_commands(commands_file)
    if not commands:
        print("No commands saved.")
        return
    items = sorted(commands.items(), key=lambda x: commands[x[0]].get('use_count', 0), reverse=True)
    def tui(stdscr):
        curses.curs_set(0)
        idx = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Shell Keeper - {} Mode".format("Remove" if remove_mode else "Retrieve"))
            for i, (name, info) in enumerate(items):
                line = f"> {name}: {info['command']}" if i == idx else f"  {name}: {info['command']}"
                stdscr.addstr(i+2, 0, line)
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_UP:
                idx = (idx - 1) % len(items)
            elif key == curses.KEY_DOWN:
                idx = (idx + 1) % len(items)
            elif key in [curses.KEY_ENTER, 10, 13]:
                name, info = items[idx]
                if remove_mode:
                    del commands[name]
                    save_commands(commands, commands_file)
                    items.pop(idx)
                    if not items:
                        stdscr.clear()
                        stdscr.addstr(0, 0, "All commands deleted.")
                        stdscr.refresh()
                        stdscr.getch()
                        break
                    idx = min(idx, len(items)-1)
                else:
                    # Copy to clipboard and print
                    try:
                        pyperclip.copy(info['command'])
                        stdscr.clear()
                        stdscr.addstr(0, 0, f"Copied: {info['command']}")
                        stdscr.refresh()
                        stdscr.getch()
                    except Exception:
                        stdscr.clear()
                        stdscr.addstr(0, 0, f"Command: {info['command']}")
                        stdscr.refresh()
                        stdscr.getch()
                    # Increment use_count
                    info['use_count'] = info.get('use_count', 0) + 1
                    commands[name] = info
                    save_commands(commands, commands_file)
                    break
            elif key == 27:  # ESC
                break
    curses.wrapper(tui)
#!/usr/bin/env python3
import argparse
import json
import os


import sys

def get_commands_file(args=None):
    # Priority: CLI arg > ENV > default
    if args and getattr(args, 'file', None):
        return args.file
    return os.environ.get('SK_COMMANDS_FILE', 'commands.json')


def load_commands(commands_file):
    if not os.path.exists(commands_file):
        return {}
    with open(commands_file, 'r') as f:
        return json.load(f)

def save_commands(commands, commands_file):
    with open(commands_file, 'w') as f:
        json.dump(commands, f, indent=2)


def cmd_save(args):
    commands_file = get_commands_file(args)
    commands = load_commands(commands_file)
    # If command is piped in, read from stdin
    if args.command == '-' or args.command is None:
        cmd = sys.stdin.read().strip()
    else:
        cmd = args.command
    commands[args.name] = {
        'command': cmd,
        'description': args.description or ''
    }
    save_commands(commands, commands_file)
    print(f"Saved command '{args.name}'.")


def cmd_list(args):
    commands_file = get_commands_file(args)
    commands = load_commands(commands_file)
    if not commands:
        print("No commands saved.")
        return
    for name, info in commands.items():
        desc = info.get('description', '')
        print(f"{name}: {info['command']}" + (f"\n  {desc}" if desc else ''))


def cmd_get(args):
    commands_file = get_commands_file(args)
    commands = load_commands(commands_file)
    info = commands.get(args.name)
    if not info:
        print(f"No command found with name '{args.name}'.")
        return
    print(info['command'])



def main():
    parser = argparse.ArgumentParser(description='Shell Keeper (sk): Save and retrieve shell commands.')
    parser.add_argument('-f', '--file', help='Path to commands JSON file')
    parser.add_argument('-rm', action='store_true', help='Remove mode: interactively delete commands')
    subparsers = parser.add_subparsers(dest='command')

    save_parser = subparsers.add_parser('save', help='Save a shell command')
    save_parser.add_argument('name', help='Name for the command')
    save_parser.add_argument('command', nargs='?', default=None, help='The shell command to save, or - to read from stdin')
    save_parser.add_argument('-d', '--description', help='Description of the command')
    save_parser.add_argument('-f', '--file', help='Path to commands JSON file')
    save_parser.set_defaults(func=cmd_save)

    list_parser = subparsers.add_parser('list', help='List saved commands')
    list_parser.add_argument('-f', '--file', help='Path to commands JSON file')
    list_parser.set_defaults(func=cmd_list)

    get_parser = subparsers.add_parser('get', help='Retrieve a saved command')
    get_parser.add_argument('name', help='Name of the command to retrieve')
    get_parser.add_argument('-f', '--file', help='Path to commands JSON file')
    get_parser.set_defaults(func=cmd_get)

    args = parser.parse_args()
    if args.command is None:
        # Interactive mode
        commands_file = get_commands_file(args)
        interactive_mode(commands_file, remove_mode=args.rm)
    elif hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
