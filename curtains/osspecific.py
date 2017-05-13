import getpass
import sys
import subprocess
from curtains.state import env


__all__  = ["win_command_loop"]


def win_make_commands(commands):
    # get smarter about it
    return [([c['cmd'] for c in commands], True)]


def win_command_loop(commands, username=None, password=None, hosts=None):
    username = username or env.get("username")
    password = password or env.get("password")
    hosts = hosts or env.get("hosts")
    command_batches = win_make_commands(commands)

    auth_cmd = win_get_credential(username, password)
    for cmd_list, remote in command_batches:
        if remote:
            processes = []
            for cmpt_name in hosts:
                # cmpt_name = % i
                invoke_cmd = win_invoke_command(cmpt_name, cmd_list)
                cmd = auth_cmd + invoke_cmd
                print("Executing on machine %s" % cmpt_name)
                proc = subprocess.Popen(["powershell.exe", "-ExecutionPolicy",
                                         'RemoteSigned', "-Command",
                                         ";".join(cmd)
                                         ],
                                        stdout=sys.stdout, stderr=sys.stderr)
                processes.append(proc)
            for proc in processes:
                out, err = proc.communicate()


def win_invoke_command(computer_name, remote_commands):
    remote_script = ' "&" '.join(remote_commands)
    #cmd = ['Invoke-Command -computername %s -credential $cred -ScriptBlock { & cmd.exe /c %s }' % \
    cmd = ['Invoke-Command -computername %s -ScriptBlock { & cmd.exe /c %s }' % (computer_name, remote_script)]
    return cmd


def win_get_credential(username=None, password=None):
    current_user = getpass.getuser()
    username = username or current_user
    stripped_user = username.split("\\")[-1]
    need_auth = stripped_user != current_user
    if (password is None) and need_auth:
        password = getpass.getpass("Provide password for %s: " % username)

    cmd = []
    if need_auth:
        cmd = ['$passwd=convertto-securestring -AsPlainText -Force -String "%s"' % password,
               '$cred=new-object -typename System.Management.Automation.PSCredential -argumentlist "%s", $passwd' % username]
    return []
