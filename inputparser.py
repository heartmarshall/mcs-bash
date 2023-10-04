import sys
from typing import List


class InputParser:
    _input: str

    def run(self):
        for line in sys.stdin:
            self.read_input(line)

    def read_input(self, input_line: str) -> str:
        """
        Принимает строку, удаляет лишние пробелы и сохраняет в self._input.
    
        Parameters:
        -input_line: Входная строка для обработки.

        Returns:
        -Оригинальная входная строка после удаления лишних пробелов 
        """
        self._input = input_line.strip()
        return input_line

    def parse_commands(self) -> List[str]:
        """
        Разбивает текущую входную строку на список команд, используя разделитель " | ".
        
        Returns:
        -Список команд.
        """
        commands = self._input.split(' | ')
        if len(commands) == 1 and not commands[0]:
            return []
        return commands





