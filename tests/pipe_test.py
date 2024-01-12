import unittest
from unittest.mock import patch
from pipe import Pipe
from env import ENV
import subprocess


class TestPipe(unittest.TestCase):
    def setUp(self):
        self.env = ENV()
        self.env.env['TEST_KEY'] = 'TEST_VALUE'
    
    def test_execute_command_with_input(self):
        pipe = Pipe(command="echo", env=self.env, args=["Hello, World!"], input=b"Test input\n")
        result = pipe.execute_command()
        self.assertEqual(result, b"Hello, World!\n")
        
    def test_execute_command_without_input(self):
        pipe = Pipe(command="echo", env=self.env, args=["Hello, World!"])
        result = pipe.execute_command()
        self.assertEqual(result, b"Hello, World!\n")
        
    def test_execute_command_with_error(self):
        pipe = Pipe(command="non_existent_command", env=self.env)
        with self.assertRaises(FileNotFoundError):
            pipe.execute_command()
            
    def test_update_env(self):
        pipe = Pipe(command="VAR=NEW_VALUE", env=self.env)
        pipe._update_env("VAR=NEW_VALUE")
        self.assertEqual(self.env.env['VAR'], 'NEW_VALUE')

    @patch('subprocess.run')
    def test_execute_command_with_shell(self, mock_subprocess_run):
        pipe = Pipe(command="echo", env=self.env, args=["Hello, World!"], input=b"Test input\n")
        mock_subprocess_run.return_value.stdout = b"Hello, World!\n"
        result = pipe.execute_command()
        self.assertEqual(result, b"Hello, World!\n")
        mock_subprocess_run.assert_called_once_with(["echo", "Hello, World!"], input=b"Test input\n", shell=False, check=True, stdout=subprocess.PIPE)

    def test_grep_from_input(self):
        pipe = Pipe(command="grep", env=self.env, args=["input$"], input=b"Test input\n")
        result = pipe.execute_command()
        self.assertEqual(result, b"Test input\n")

    def test_grep_from_file(self):
        pipe = Pipe(command="grep", env=self.env, args=["Stas", "test.txt"])
        result = pipe.execute_command()
        self.assertEqual(result, b"my name is Stas\nwhat is your name? i am just hear my name Stas\n")

    def test_grep_with_arguments(self):
        pipe = Pipe(command="grep", env=self.env, args=["-i", "stas", "test.txt"])
        result = pipe.execute_command()
        self.assertEqual(result, b"my name is Stas\nwhat is your name? i am just hear my name Stas\n")

        pipe = Pipe(command="grep", env=self.env, args=["-w", "Stas", "test.txt"])
        result = pipe.execute_command()
        self.assertEqual(result, b"my name is Stas\nwhat is your name? i am just hear my name Stas\n")

        pipe = Pipe(command="grep", env=self.env, args=["-w", "tas", "test.txt"])
        result = pipe.execute_command()
        self.assertEqual(result, b"")

        pipe = Pipe(command="grep", env=self.env, args=["-iw", "stas", "test.txt"])
        result = pipe.execute_command()
        self.assertEqual(result, b"my name is Stas\nwhat is your name? i am just hear my name Stas\n")

        pipe = Pipe(command="grep", env=self.env, args=["-A 2", "Stas", "test.txt"])
        result = pipe.execute_command()
        self.assertEqual(result, b"my name is Stas\nwhat is your name? i am just hear my name Stas\nare you hear "
                                 b"this?\n")

    def test_grep_with_regular_expressions(self):
        pipe = Pipe(command="grep", env=self.env, args=["^hello!$", "test.txt"])
        result = pipe.execute_command()
        self.assertEqual(result, b"hello!\n")

        pipe = Pipe(command="grep", env=self.env, args=["^my", "test.txt"])
        result = pipe.execute_command()
        self.assertEqual(result, b"my name is Stas\n")

        pipe = Pipe(command="grep", env=self.env, args=["^my$", "test.txt"])
        result = pipe.execute_command()
        self.assertEqual(result, b"")

        pipe = Pipe(command="grep", env=self.env, args=["Stas$", "test.txt"])
        result = pipe.execute_command()
        self.assertEqual(result, b"my name is Stas\nwhat is your name? i am just hear my name Stas\n")


if __name__ == '__main__':
    unittest.main()
