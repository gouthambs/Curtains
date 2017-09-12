
__all__ = ['run', 'local']


class Operation(object):
    _cmd = []

    @classmethod
    def clear_commands(cls):
        cls._cmd.clear()

    @classmethod
    def commands(cls):
        return cls._cmd


class Run(Operation):
    def __call__(self, cmd):
        self._cmd.append({'cmd': cmd, 'remote': True, 'class': 'Run'})


class Local(Operation):
    def __call__(self, cmd):
        self._cmd.append({'cmd':cmd, 'remote': False, 'class': 'Local'})


class XCopy(Operation):
    def __call__(self, localpath, remotepath):
        pass


run = Run()
local = Local()