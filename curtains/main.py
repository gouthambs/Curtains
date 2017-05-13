import os
import click
import inspect
from functools import wraps
from curtains.commands import Command
from curtains.osspecific import win_command_loop


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


def main(curtfile=None, importer=None):
    if importer is None:
        importer = __import__

    print(curtfile)
    exec(open(curtfile).read())
    cli = create_cli()
    cli()


if __name__ == '__main__':
    main(os.path.join(os.getcwd(), "curtfile.py"))