import sys

from command_executor import CommandsExecutor
from command_parser import CommandParser
from env import ENV
from inputparser import InputParser


def main():
    env = ENV()

    input_parser = InputParser()
    command_parser = CommandParser(env=env)
    command_executor = CommandsExecutor(
        command_parser=command_parser,
    )

    for line in sys.stdin:
        input_parser.read_input(line)
        commands = input_parser.parse_commands()

        command_executor.execute(commands)


if __name__ == '__main__':
    main()
