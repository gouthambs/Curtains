
__all__ = ['run', 'local']


class Command(object):
    _cmd = []

    @classmethod
    def clear_commands(cls):
        cls._cmd.clear()

    @classmethod
    def commands(cls):
        return cls._cmd


class Run(Command):
    def __call__(self, cmd):
        self._cmd.append({'cmd': cmd, 'type': 'batch', 'class': 'Run'})


class Local(Command):
    def __call__(self, cmd):
        self._cmd.append({'cmd':cmd, 'type': 'batch', 'class': 'Local'})


def XCopy(Command):
    def __call__(self, localpath, remotepath):
        pass


run = Run()
local = Local()