from __future__ import print_function
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class Runner:

    def __init__(self, tool='py.test'):
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

if __name__ == '__main__':
    tool = sys.argv[1]
    watched_dir = sys.argv[2]

    FileDaemon(watched_dir, runner=Runner(tool)).init()
