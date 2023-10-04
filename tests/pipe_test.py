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
        self.assertEqual(result, b"Test input\nHello, World!\n")
        
    def test_execute_command_without_input(self):
        pipe = Pipe(command="echo", env=self.env, args=["Hello, World!"])
        result = pipe.execute_command()
        self.assertEqual(result, b"Hello, World!\n")
        
    def test_execute_command_with_error(self):
        pipe = Pipe(command="non_existent_command", env=self.env)
        with self.assertRaises(subprocess.CalledProcessError):
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
        mock_subprocess_run.assert_called_once_with(["echo", "Hello, World!"], input=b"Test input\n", shell=True, check=True, stdout=subprocess.PIPE)
        
    @patch('subprocess.run')
    def test_execute_command_without_shell(self, mock_subprocess_run):
        pipe = Pipe(command="echo", env=self.env, args=["Hello, World!"], input=b"Test input\n")
        mock_subprocess_run.return_value.stdout = b"Hello, World!\n"
        result = pipe.execute_command()
        self.assertEqual(result, b"Hello, World!\n")
        mock_subprocess_run.assert_called_once_with(["echo", "Hello, World!"], input=b"Test input\n", shell=False, check=True, stdout=subprocess.PIPE)
        
if __name__ == '__main__':
    unittest.main()
