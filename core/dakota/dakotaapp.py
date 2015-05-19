# Standard Python modules
# =======================
import os

# DICE modules
# ============
from core.app import BasicApp


class DakotaApp(BasicApp):
    app_name = "NoNameDakotaApp"

    def __init__(self, parent, instance_name, status):
        BasicApp.__init__(self, parent, instance_name, status)

        self.dakota_input_file = None
        self.dakota_input_file_name = None

    def register_dakota_file(self, path, var):
        self.dakota_input_file_name = path
        self.dakota_input_file = var
        self.signal(path)

    def get_dakota_var(self, path=None):
        if path is None:
            return None
        var_path = self.split_path(path)
        return self.get_dakota_value_by_path(var_path)

    def get_dakota_value_by_path(self, path):
        return self.get_value_by_path(self.dakota_input_file, path)

    def set_dakota_var(self, path, value):
        var_path = self.split_path(path)
        var = self.dakota_input_file
        py_dakota_var = self.get_dict_by_path(self.dakota_input_file, var_path)
        try:
            py_dakota_var['value'] = value
        except TypeError:
            try:
                if value == "$invalid$":
                    return
                # else:
                    # py_dakota_var[int(var_path[-1])] = value
            except ValueError:
                raise KeyError("Could not set "+str(path)+" to "+str(value)+" (in "+str(py_dakota_var)+")")

        var.writeFile()
        self.signal(self.dakota_input_file_name, var_path, value)

    def dakota_var_signal_name(self, path=None):
        if path is not None:
            # self.debug("fv "+file_name)  # TODO: check why we get paths like 0
            return self.dakota_input_file_name
        else:
            return None

    @staticmethod
    def split_path(path):
        '''
        convert path to list
        '''
        if isinstance(path, str):
            tmp_path = path.split(" ")
            path = []
            for i in tmp_path:
                path.append(i)
                path.append('child')
            path[-1] = 'value'
        elif isinstance(path, int):
            path = str(path)
        return path

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
