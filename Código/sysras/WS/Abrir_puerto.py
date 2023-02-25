#!/usr/bin/python
import sys
import subprocess, shlex
comando1='sudo rfcomm connect hci 94:E6:86:DA:EA:6A'
args=shlex.split(comando1)
subprocess.call(args)
