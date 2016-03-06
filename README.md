# mojo - continuous test runner

Heavily inspired by `tdaemon` tool which automatically triggers tests on any change in pointed directory. Created because `tdaemon` doesn't support python 3.

## Usage

Run:

    $ python /path/to/mojo.py

mojo will start to monitor the current directory and will trigger `py.test` on any change.

To use different testing tool use `-t` parameter:

    $ python /path/to/mojo.py -t nose

Will run your tests using `nosetests` runner.

In order watch custom directory issue:

    $ python /path/to/mojo.py -d /path/to/your/project

# Supported tools

* [nosetests](http://somethingaboutorange.com/mrl/projects/nose/)
* [py.test](http://codespeak.net/py/dist/test.html)
