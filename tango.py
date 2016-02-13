from __future__ import print_function
import time
import subprocess
import click
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class Runner:

    def __init__(self, tool):
        self.tool = tool

    def execute(self, directory='.'):
        subprocess.call([self.tool, directory])


class FileDaemon(PatternMatchingEventHandler):

    def __init__(self, watched_dir, runner, interval=2):
        super().__init__(ignore_directories=True)
        self.watched_dir = watched_dir
        self.runner = runner
        self.interval = interval

    def on_created(self, event):
        print('{} {} {}'.format(self.runner, event.src_path, event.event_type))
        self.runner.execute(self.watched_dir)

    def init(self):
        observer = Observer()
        observer.schedule(self, self.watched_dir)
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
def tango(test_runner, directory):
    FileDaemon(watched_dir=directory, runner=Runner(tool=test_runner)).init()


if __name__ == '__main__':
    tango()
