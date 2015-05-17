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
        dakota_bin_path = self.dice.settings.value(self, ['DAKOTA', 'dakota'])[:-7]
        dakota_lib_path = self.dice.settings.value(self, ['DAKOTA', 'dakota'])[:-10] + "lib"
        dakota_test_path = self.dice.settings.value(self, ['DAKOTA', 'dakota'])[:-10] + "test"
        os_dakota_ld_library_path = ":" + dakota_bin_path + ":" + dakota_lib_path
        os_dakota_path = ":" + dakota_bin_path + ":" + dakota_test_path

        os.environ['LD_LIBRARY_PATH'] += os_dakota_ld_library_path
        os.environ['PATH'] += os_dakota_path

        f_args = [self.dice.settings.value(self, ['DAKOTA', 'dakota'])]
        f_args.extend(args)
        cwd = self.current_run_path()
        result = self.run_process(f_args, stdout=stdout, stderr=stderr, cwd=cwd, env=os.environ)
        return result