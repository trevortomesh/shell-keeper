
# Shell Keeper (sk)

Shell Keeper is a command-line tool to save, retrieve, and manage your favorite shell commands. It features interactive navigation, clipboard integration, and customizable storage location.

## Features

- Save shell commands with a name and description
- Retrieve commands interactively (arrow keys, Enter to copy)
- Remove commands interactively
- Store commands in a JSON file (customizable location)
- Installable as a global executable (`sk`)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/trevortomesh/shell-keeper.git
   cd shell-keeper
   ```

2. Install with pip:

   ```sh
   pip install .
   ```

   This will make the `sk` command available globally.

## Usage

### Save a command

```sh
sk save <name> '<shell command>' -d 'description'
```

Or pipe a command:

```sh
echo "ls -la" | sk save mylist -
```

### List commands

```sh
sk list
```

### Retrieve a command interactively

```sh
sk
```

Use arrow keys to navigate, Enter to copy to clipboard.

### Remove a command interactively

```sh
sk -rm
```

Use arrow keys to select, Enter to delete.

### Custom JSON file location

Set with environment variable or CLI flag:

```sh
export SK_COMMANDS_FILE=~/my_commands.json
sk save ...
```

Or:

```sh
sk save ... -f ~/my_commands.json
```

## Requirements

- Python 3
- `pyperclip` (installed automatically)

## License

MIT
