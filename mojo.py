from __future__ import print_function
import time
import subprocess
import click
import hashlib
from collections import defaultdict
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class Runner:

    def __init__(self, tool):
        self.tool = tool

    def execute(self, directory='.'):
        subprocess.call([self.tool, directory])


class FileDaemon(PatternMatchingEventHandler):

    def __init__(self, watched_dir, runner, interval=2):
        super().__init__(ignore_patterns=['*.pyc'], ignore_directories=True)
        self.watched_dir = watched_dir
        self.runner = runner
        self.interval = interval
        self._cache = defaultdict(str)

    def _hashcode(self, path):
        content = open(path).read()
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
@click.option('-t', '--test_runner', default='py.test', type=str)
@click.option('-d', '--directory', default='.', type=str)
def mojo(test_runner, directory):
    FileDaemon(watched_dir=directory, runner=Runner(tool=test_runner)).init()


if __name__ == '__main__':
    mojo()
