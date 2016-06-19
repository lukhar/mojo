from __future__ import print_function
from builtins import super, open
import time
import hashlib
import click
from collections import defaultdict
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from . import runner


class FileDaemon(PatternMatchingEventHandler):

    def __init__(self, watched_dir, runner, blacklist=None, interval=2):
        super().__init__(patterns=['*.py'], ignore_directories=True)
        self.watched_dir = watched_dir
        self.runner = runner
        self.interval = interval
        self.blacklist = blacklist
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
        self.runner.execute(self.watched_dir, self.blacklist)

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
@click.option('-i', '--ignore', multiple=True, type=click.Path())
def mojo(test_runner, directory, ignore):
    FileDaemon(watched_dir=directory, blacklist=ignore, runner=runner.create(tool=test_runner)).init()
