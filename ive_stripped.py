import venv
import subprocess
import sys

def make_ive(path, packages):
    venv.create(path)
    vi = sys.version_info
    subprocess.run([sys.executable, '-m', 
                    'pip', 'install', ' '.join(packages), 
                    f'--target={path}/lib/python{vi.major}.{vi.minor}/site-packages'], capture_output=True)

def main_automatic(name, packages, path=None):
    if path == None:
        path = name
    make_ive(path, packages)

def main_interactive():
    name = input('Enter the name for the virtualenv: ')
    packages = input('Enter a space-separated list of packages to install: ').strip().split()
    main_automatic(name, packages, name)

args = sys.argv[1:]
if args:
    main_automatic(args[0], args[1:])
else:
    main_interactive()
