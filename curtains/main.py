import os
import click
import inspect
from functools import wraps
from curtains.commands import Command
from curtains.osspecific import win_command_loop
from curtains import state


@click.group(chain=True)
@click.pass_context
def cli(ctx):
    pass


@cli.resultcallback()
def process_result(result, **kwargs):
    pass


def cmd_loop(commands, env):
    if os.name == 'nt':
        win_command_loop(commands, **env)
    else:
        raise NotImplementedError("Unsupported OS type "+os.name)


def executor(fn, env):
    @wraps(fn)
    def decorated(*args, **kwargs):
        Command.clear_commands()
        fn(*args, **kwargs)
        cmd_loop(Command.commands(), env)
    return decorated


def create_cli():
    from curtains.decorator import task
    task_list = task.task_list()
    #task_fn = [t['fn'], t) for t in task_list]
    for task in task_list:
        t = task.pop('fn')
        argnames = [str(a) for a in inspect.signature(t).parameters.keys()]
        fn = executor(t, task)
        for arg in argnames[::-1]:
            click.argument(arg)(fn)
        cli.command()(fn)
    return cli

def _is_package(path):
    """
    Is the given path a Python package?
    """
    _exists = lambda s: os.path.exists(os.path.join(path, s))
    return (
        os.path.isdir(path)
        and (_exists('__init__.py') or _exists('__init__.pyc'))
    )


def find_curtfile(names=None):
    """
    Attempt to locate a fabfile, either explicitly or by searching parent dirs.
    Usage docs are in sites/docs/usage/fabfiles.rst, in "Fabfile discovery."
    """
    # Obtain env value if not given specifically
    if names is None:
        names = [state.env["curtfile"]]
    # Create .py version if necessary
    if not names[0].endswith('.py'):
        names += [names[0] + '.py']
    # Does the name contain path elements?
    if os.path.dirname(names[0]):
        # If so, expand home-directory markers and test for existence
        for name in names:
            expanded = os.path.expanduser(name)
            if os.path.exists(expanded):
                if name.endswith('.py') or _is_package(expanded):
                    return os.path.abspath(expanded)
    else:
        # Otherwise, start in cwd and work downwards towards filesystem root
        path = '.'
        # Stop before falling off root of filesystem (should be platform
        # agnostic)
        while os.path.split(os.path.abspath(path))[1]:
            for name in names:
                joined = os.path.join(path, name)
                if os.path.exists(joined):
                    if name.endswith('.py') or _is_package(joined):
                        return os.path.abspath(joined)
            path = os.path.join('..', path)


def main(curtfile_locations=None):
    curtfile = find_curtfile(curtfile_locations)
    print(curtfile)
    exec(open(curtfile).read())
    cli = create_cli()
    cli()


if __name__ == '__main__':
    main(os.path.join(os.getcwd(), "curtfile.py"))