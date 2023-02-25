import shlex, subprocess

command_line= 'sudo pppd call gprs'

args = shlex.split(command_line)
subprocess.call(args)

