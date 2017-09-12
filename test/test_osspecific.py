from curtains.api import run, local
from curtains.operations import Operation
from curtains.osspecific import win_make_commands


def test_win_command_loop():
    Operation.clear_commands()
    run("echo Hello World")
    run("dir")
    local("echo Hello World")
    local("dir")
    run("echo Bye Bye")
    expected = [{'cmd': "echo Hello World", 'remote': True, 'class': 'Run'},
                {'cmd': "dir", 'remote': True, 'class': 'Run'},
                {'cmd': "echo Hello World", 'remote': False, 'class': 'Local'},
                {'cmd': "dir", 'remote': False, 'class': 'Local'},
                {'cmd': "echo Bye Bye", 'remote': True, 'class': 'Run'}]
    assert Operation.commands() == expected
    return


def test_win_make_command():
    Operation.clear_commands()
    run("echo Hello World")
    run("dir")
    local("echo Hello World")
    local("dir")
    run("echo Bye Bye")
    cmds = Operation.commands()
    res = win_make_commands(cmds)
    expected = [(["echo Hello World", "dir"], True),
                (["echo Hello World", "dir"], False),
                (["echo Bye Bye"], True)]
    assert res == expected
    return