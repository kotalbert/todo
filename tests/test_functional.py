import unittest
from queue import Queue
from threading import Thread

from src.todo.app import TODOApp


class TestTODOFunctional(unittest.TestCase):
    def setUp(self) -> None:
        self.inputs = Queue()
        self.outputs = Queue()

        self.fake_output = lambda txt: self.outputs.put(txt)
        self.fake_input = lambda: self.inputs.get()

    def send_input(self, txt):
        self.inputs.put(txt)

    def get_output(self):
        return self.outputs.get()

    def test_main(self):
        app = TODOApp(io=(self.fake_input, self.fake_output))

        app_thread = Thread(target=app.run, daemon=True)
        app_thread.start()

        welcome = self.get_output()
        expected_welcome = ('TODOs:\n'
                            '\n'
                            '\n'
                            '> ')
        self.assertEqual(welcome, expected_welcome)

        self.send_input('add buy milk')
        todos1 = self.get_output()
        expected_todos1 = ('TODOs:\n'
                           '1. buy milk\n'
                           '\n'
                           '> ')
        self.assertEqual(todos1, expected_todos1)

        self.send_input('add buy eggs')
        todos2 = self.get_output()
        expected_todos2 = ('TODOs:\n'
                           '1. buy milk\n'
                           '2. buy eggs\n'
                           '\n'
                           '> ')
        self.assertEqual(todos2, expected_todos2)

        self.send_input('del 1')
        todos3 = self.get_output()
        self.assertEqual(todos3, expected_todos1)

        self.send_input('quit')
        app_thread.join(1)
        self.assertEqual(self.get_output(), 'bye!')
