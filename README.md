# mojo - continuous test runner

Heavily inspired by `tdaemon` tool which automatically triggers tests on any change in pointed directory. Created because `tdaemon` doesn't support python 3.

## Usage

Install:

    $ pip install git+https://github.com/lukhar/mojo

Run:

    $ mojo

mojo will start to monitor the current directory and will trigger `py.test` on any change.

To use different testing tool use `-t` parameter:

    $ mojo -t nose

Will run your tests using `nosetests` runner.

In order watch custom directory issue:

    $ mojo -d /path/to/your/project

# Supported tools

* [nosetests](https://nose.readthedocs.org/en/latest/)
* [py.test](http://pytest.org/latest/)
