"""
BashTerminal
============
DICE Bash terminal

Copyright (c) 2014-2015 by DICE Developers
All rights reserved.
"""

# Standard Python modules
# =======================
import subprocess
from threading import Thread

# DICE modules
# ============
from core.app import BasicApp


class BashTerminal(BasicApp):
    """
    BashTerminal
    ============
    """

    app_name = "BashTerminal"
    input_types = []
    output_types = []

    def __init__(self, parent, instance_name, status):
        """
        Constructor of bashTerminal
        :param parent:
        :param instance_name:
        :param status:
        :return:
        """

        BasicApp.__init__(self, parent, instance_name, status)

        self.bash = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.reader = BashIOReader(self.bash.stdout, self.emit_stdout, self.debug)
        self.reader.start()

        self.err_reader = BashIOReader(self.bash.stderr, self.emit_stdout, self.debug)
        self.err_reader.start()

    def emit_stdout(self, c):
        self.log(c)

    def send_key(self, key):
        self.bash.stdin.write(key)
        self.bash.stdin.flush()

    def run(self):
        self.reader.run()


class BashIOReader(Thread):

    def __init__(self, stdout, callback, debug=None):
        Thread.__init__(self)
        self.stdout = stdout
        self.callback = callback
        self.debug = debug

    def run(self):
        if self.debug:
            self.debug("starting reader")
        for line in iter(self.stdout.readline, ''):
            self.signal(line.rstrip("\n"))