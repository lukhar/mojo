from __future__ import print_function
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileDaemon(FileSystemEventHandler):

    def __init__(self, watched_dir, runner):
        self.watched_dir = watched_dir
        self.runner = runner

    def on_created(self, event):
        print('hello ' + event.src_path)
        subprocess.call(['py.test'])

    def init(self):
        observer = Observer()
        observer.schedule(self, self.watched_dir)
        observer.start()

        print('started on: ' + self.watched_dir)
        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == '__main__':
    watched_dir = sys.argv[1]

    FileDaemon(watched_dir, runner=None).init()
