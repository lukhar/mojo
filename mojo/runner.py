import pkgutil
import sys
import subprocess
from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass


class Runner(with_metaclass(ABCMeta)):

    @abstractmethod
    def execute(self, directory='.', blacklist=None):
        pass


class PyTestRunner(Runner):

    def execute(self, directory='.', blacklist=None):
        if blacklist is None:
            subprocess.call(['py.test', directory])
            return

        ignore_statement = ' '.join('--ignore={}'.format(blacklisted) for blacklisted in blacklist)

        subprocess.call(['py.test', directory, ignore_statement])


class NoseTestRunner(Runner):

    def __init__(self):
        if not pkgutil.find_loader('nose_exclude'):
            print('warning: nose-exclude plugin is required to use -i option with nose.')

    def execute(self, directory='.', blacklist=None):
        if blacklist is None:
            subprocess.call(['nosetests', directory])
            return

        ignore_statement = ' '.join('--exclude-dir={}'.format(blacklisted) for blacklisted in blacklist)
        subprocess.call(['nosetests', directory, ignore_statement])


def create(tool):
    if not pkgutil.find_loader(tool if tool != 'py.test' else 'pytest'):
        sys.exit('{} is not installed on your system.'.format(tool))
    elif tool == 'py.test':
        return PyTestRunner()
    elif tool == 'nose':
        return NoseTestRunner()
    else:
        raise Exception('{} is not yet supported.'.format(tool))
