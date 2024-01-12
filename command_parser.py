import re

from env import ENV
from pipe import Pipe


class CommandParser:
    def __init__(self, env: ENV, variable_pattern='\$([a-zA-Z_][a-zA-Z0-9_]*)') -> None:
        self.variable_pattern = rf"{variable_pattern}"
        self.env = env

    def parse_command(self, row_command_text: str):
        """
        Парсит row_command_text и делает из него Pipe

        Parameters:
        -row_command_text (str): текст команды, которую нужно распарсить

        Returns:
        -Pipe: объект Pipe, представляющий собой готовую к выполнению команду.
        """
        command_text = ""
        row_command_text = row_command_text.split("'")
        for i, command_part in enumerate(row_command_text):
            if i % 2 != 0:
                command_text += f"'{command_part}'"
                continue
            variables = re.findall(self.variable_pattern, command_part)
            for var in variables:
                if var in self.env.env:
                    command_part = command_part.replace(f'${var}', self.env.env[var])
            command_text += command_part

        splits = command_text.split(maxsplit=1)
        command, arguments = splits[0], splits[1:]

        # Обработка аргументов и присвоений отдельно от команды
        if '=' in command:
            arguments = ''
        elif len(arguments) != 0:
            arguments = arguments[0].split(' ')

        return Pipe(
            command=command,
            env=self.env,
            args=arguments,
        )
