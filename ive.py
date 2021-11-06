import venv
import subprocess
import sys
import pathlib
from typing import *

def help_s(s: str):
    print(f'[\033[94mHELP\033[0m] {s}')

def info(s: str):
    print(f'[\033[92mINFO\033[0m] {s}')

def error(s: str, exit_p: int = 0):
    print(f'[\033[91mERROR\033[0m] {s}')
    if exit_p != 0:
        sys.exit(exit_p)

def prompt(s: str, default: Optional[str] = None):
    ret = input(f'[\033[33mPROMPT\033[0m] {s}')
    if not default:
        while not ret:
            print('[\033[33mPROMPT\033[0m] Please enter a value.')
            ret = input(f'[\033[33mPROMPT\033[0m] {s}')
    return ret if ret else default

def make_ive(path: str, packages: Sequence[str]):
    venv.create(path)
    info('Created empty virtual environment')
    vi = sys.version_info
    info('Installing packages')
    if subprocess.run([sys.executable, '-m', 
                    'pip', 'install', ' '.join(packages), 
                    f'--target={path}/lib/python{vi.major}.{vi.minor}/site-packages'], capture_output=True).returncode:
        error('pip ran into an error. Terminating.', 1)
    info('Installed all packages')

def main_automatic(name: str, packages: Sequence[str], path: Optional[str] = None):
    if path == None:
        path = name
    make_ive(path, packages)

def main_interactive():
    name = prompt('Enter the name for the virtualenv: ')
    packages = prompt('Enter a space-separated list of packages to install: ').strip().split()
    path = prompt(f'Enter the location of the virtualenv [./{name}]: ', default=name)
    main_automatic(name, packages, path)

args = sys.argv[1:]
if args:
    if '--help' in args or '-h' in args:
        help_s('python ive.py [NAME PACKAGE [P P ...]]')
        help_s('When run with no arguments, enter interactive mode.')
        help_s('    NAME: The name of the virtualenv (created in the current directory)')
        help_s('    PACKAGE: The packages to install')
    elif len(args) == 1:
        error('Number of args must be 0 or greater than 2.', 1)
    else:
        main_automatic(args[0], args[1:])
else:
    main_interactive()
