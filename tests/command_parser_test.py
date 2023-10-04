from command_parser import CommandParser
from env import ENV

import unittest

class TestCommandParser(unittest.TestCase):
    def setUp(self):
        self.env = ENV()
        self.env.env = {'VAR1': 'value1', 'VAR2': 'value2'}
        self.parser = CommandParser(self.env)

    def test_parse_command_with_variables(self):
        result = self.parser.parse_command('echo $VAR1 $VAR2')
        self.assertEqual(result.command, 'echo')
        self.assertEqual(result.args, ['value1', 'value2'])

    def test_parse_command_with_single_quoted_string(self):
        result = self.parser.parse_command("echo 'Hello, $VAR1'")
        self.assertEqual(result.command, 'echo')
        self.assertEqual(result.args, ['Hello, $VAR1'])

    def test_parse_command_with_variable_not_in_env(self):
        result = self.parser.parse_command('echo $VAR3')
        self.assertEqual(result.command, 'echo')
        self.assertEqual(result.args, ['$VAR3'])

    def test_parse_command_with_assignment(self):
        result = self.parser.parse_command('VAR3=value3')
        self.assertEqual(result.command, 'VAR3=value3')
        self.assertEqual(result.args, '')

if __name__ == '__main__':
    unittest.main()
