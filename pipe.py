import subprocess
from typing import List, Any

from attr import attrs, attrib

from env import ENV


@attrs
class Pipe:
    command: str = attrib()
    env: ENV = attrib()
    args: List[Any] = attrib(default=[])
    input: bytes = attrib(default='')

    def execute_command(self) -> bytes:
        """
        Иполняет команду, которая записана в self.command. При этом используются аргументы из self.args.

        Returns:
        -Вывод исполняемой программы в виде байтовой последовательности
        """
        shell = False
        if '=' in self.command:
            shell = True

        try:
            process = subprocess.run(
                [self.command, *self.args],
                input=self.input,
                shell=shell,
                check=True,
                stdout=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            print(f"Command error {e.cmd}!")
            raise e
        else:
            output = process.stdout

        self._update_env(self.command)

        return output

    def _update_env(self, command: str):
        if '=' in command:
            key, value = command.split('=')
            self.env.env[key] = value










