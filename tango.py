import os


class Crawler:

    def crawl(self, path):
        files = {}
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                files[os.path.join(dirpath, filename)] = 1

        return files
