import unittest
from ..inputparser import InputParser


class TestInputParser(unittest.TestCase):

    def setUp(self):
        self.parser = InputParser()

    def test_read_input(self):
        input_line = "  This is a test input  "
        expected_result = "This is a test input"
        result = self.parser.read_input(input_line)
        self.assertEqual(result, expected_result)
        self.assertEqual(self.parser._input, expected_result)

    def test_parse_commands(self):
        self.parser._input = "command1 | command2 | command3"
        expected_result = ["command1", "command2", "command3"]
        result = self.parser.parse_commands()
        self.assertEqual(result, expected_result)

    def test_parse_commands_no_input(self):
        self.parser._input = ""
        expected_result = []
        result = self.parser.parse_commands()
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()

