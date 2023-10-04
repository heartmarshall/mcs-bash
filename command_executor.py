from typing import List

from command_parser import CommandParser
from pipe import Pipe


class CommandsExecutor:
    def __init__(self, command_parser: CommandParser) -> None:
        self.curr_input = ""  # мы же можем принять только позиционные аргументы?
        self.command_parser = command_parser
        self.curr_pipe = None

    def _make_pipe(self, command: str):
        """
        Создает и возвращает объект Pipe на основе переданной команды.

        Parameters:
        - command (str): Команда для создания Pipe.

        Returns:
        - Pipe: Объект Pipe, представляющий переданную команду.
        """

        new_pipe = self.command_parser.parse_command(command)
        return new_pipe

    def _evaluate_pipe(self, pipe: Pipe) -> bytes:
        """
        Выполняет текущий конвейер (pipe) с текущими аргументами и возвращает результат выполнения.

        Parameters:
        - pipe: Объект Pipe, представляющий текущую команду.

        Returns:
        - str: Результат выполнения команды в конвейере.
        """

        pipe.input = self.curr_input
        return pipe.execute_command()

    def execute(self, commands: List[str]):
        """
        Выполняет последовательность команд с использованием конвейера и возвращает конечный результат.

        Returns:
        - str: Конечный результат выполнения всех команд.
        """

        for command in commands:
            cur_pipe = self._make_pipe(command)

            try:
                self.curr_input = self._evaluate_pipe(cur_pipe)
            except Exception as e:
                print(f"Failed to execute commands: {e}")
                return

        print(self.curr_input.decode(encoding='utf8'))