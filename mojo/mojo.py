from __future__ import print_function
from builtins import super, open
import time
import subprocess
import click
import hashlib
import pkgutil
import sys
from collections import defaultdict
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class Runner:

    def __init__(self, tool, blacklist):
        if not pkgutil.find_loader(tool if tool != 'py.test' else 'pytest'):
            sys.exit('{} is not installed on your system.'.format(tool))
        self.tool = tool
        self.blacklist = blacklist

    def execute(self, directory='.'):
        if self.tool == 'py.test' and self.blacklist:
            subprocess.call([self.tool, directory, '--ignore={}'.format(self.blacklist)])
        else:
            subprocess.call([self.tool, directory])


class FileDaemon(PatternMatchingEventHandler):

    def __init__(self, watched_dir, runner, interval=2):
        super().__init__(patterns=['*.py'], ignore_directories=True)
        self.watched_dir = watched_dir
        self.runner = runner
        self.interval = interval
        self._cache = defaultdict(str)

    def _hashcode(self, path):
        with open(path, 'r') as source:
            content = source.read()
            hashcode = hashlib.md5(content.encode('utf-8')).hexdigest()
            return hashcode

    def on_created(self, event):
        if self._cache[event.src_path] == self._hashcode(event.src_path):
            return

        self._cache[event.src_path] = self._hashcode(event.src_path)
        self.runner.execute(self.watched_dir)

    def init(self):
        observer = Observer()
        observer.schedule(self, self.watched_dir, recursive=True)
        observer.start()

        print('started on: ' + self.watched_dir)
        try:
            while True:
                time.sleep(self.interval)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


@click.command()
@click.option('-t', '--test_runner', default='py.test', type=click.Choice(['nose', 'py.test']))
@click.option('-d', '--directory', default='.', type=str)
@click.option('-i', '--ignore', type=str)
def mojo(test_runner, directory, ignore):
    FileDaemon(watched_dir=directory, runner=Runner(tool=test_runner, blacklist=ignore)).init()
