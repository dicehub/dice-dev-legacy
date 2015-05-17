# Standard Python modules
# =======================
import os
import subprocess
import csv

# DICE modules
# ============
from core.app import BasicApp


class DakotaApp(BasicApp):

    app_name = "NoNameDakotaApp"

    def __init__(self, parent, instance_name, status):
        BasicApp.__init__(self, parent, instance_name, status)

        self.dakota_files = dict()

    def register_dakota_file(self, path, var):
        self.dakota_files[path] = var
        self.signal(path)

    def dakota_exec(self, args, stdout=None, stderr=None, cwd=None):

        # Set Environment
        # ===============
        os.environ['LD_LIBRARY_PATH'] += ":/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/bin:/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/lib"
        os.environ['PATH'] += ':/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/bin:/home/ros/Programs/Dakota/dakota-6.1.0.Linux.x86_64/test'

        f_args = [self.dice.settings.value(self, ['DAKOTA', 'dakota'])]
        f_args.extend(args)
        cwd = self.current_run_path()
        result = self.run_process(f_args, stdout=stdout, stderr=stderr, cwd=cwd, env=os.environ)
        return result