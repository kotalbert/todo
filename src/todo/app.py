import functools


class TODOApp:
    def __init__(self, io=(input, functools.partial(print, end=""))):
        self._in, self._out = io
        self._quit = False
        self._entries = []

    def cmd_add(self, what):
        self._entries.append(what)

    def cmd_del(self, idx):
        idx = int(idx) - 1
        if 0 > idx > len(self._entries):
            self._out('Invalid index\n')
            return
        self._entries.pop(idx)

    def cmd_quit(self):
        self._quit = True

    def run(self):
        self._quit = False
        while not self._quit:
            self._out(self.prompt(self.items_list()))
            command = self._in()
            self._dispatch(command)
        self._out('bye!')

    @staticmethod
    def prompt(output):
        return f'TODOs:\n{output}\n\n> '

    def _dispatch(self, command):
        cmd, *args = command.split(None, 1)
        executor = getattr(self, f'cmd_{cmd}', None)
        if executor is None:
            self._out(f'Invalid command {cmd}')
            return
        executor(*args)

    def items_list(self):
        enumerated_items = enumerate(self._entries, start=1)
        return '\n'.join([f'{idx}. {entry}' for idx, entry in enumerated_items])
