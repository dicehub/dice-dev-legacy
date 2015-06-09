# Standard Python modules
# =======================
import os

# DICE modules
# ============
from dice.app import BasicApp


class DakotaApp(BasicApp):
    app_name = "NoNameDakotaApp"

    def __init__(self, parent, instance_name, status):
        BasicApp.__init__(self, parent, instance_name, status)

        self.dakota_files = dict()

    def register_dakota_file(self, path, var):
        self.dakota_files[path] = var
        self.signal(path)

    # Get/Set/Signal Dakota var
    # =========================
    def get_dakota_var(self, path=None):
        if path is None:
            return None
        file_name, var_path = self.split_path(path)
        var = self.dakota_files[file_name]
        return self.get_value_by_path(var, var_path)

    def set_dakota_var(self, path, value):
        file_name, var_path = self.split_path(path)
        if file_name in self.dakota_files:
            var = self.dakota_files[file_name]
            py_dakota_var = self.get_dict_by_path(var, var_path)
            try:
                py_dakota_var[var_path[-1]] = value
            except TypeError:
                try:
                    if value == "$invalid$":
                        return
                    else:
                        py_dakota_var[int(var_path[-1])] = value
                except ValueError:
                    raise KeyError("Could not set "+str(path)+" to "+str(value)+" (in "+str(py_dakota_var)+")")

            var.writeFile()
            self.signal(file_name, var_path, value)

    def dakota_var_signal_name(self, path=None):
        if path is not None:
            file_name, _ = self.split_path(path)
            return file_name
        else:
            return None

    # Get/Set/Signal Optional Dakota keyword
    # ======================================
    def get_dakota_keyword(self, path_and_model_method):
        if path_and_model_method is None:
            return None
        path = path_and_model_method[0]
        file_name, var_path = self.split_path(path)
        var = self.dakota_files[file_name]
        dak_var = self.get_value_by_path(var, var_path)

        method_name = path_and_model_method[1]
        model_method = getattr(self, method_name)
        if len(path_and_model_method) == 3:
            model = model_method(path_and_model_method[2])
        else:
            model = model_method()
        for keyword in model:
            if keyword in dak_var:
                return keyword
        return None

    def set_dakota_keyword(self, path_and_model_method, value):
        path = path_and_model_method[0]
        file_name, var_path = self.split_path(path)
        if file_name in self.dakota_files:
            var = self.dakota_files[file_name]
            method_name = path_and_model_method[1]
            try:
                # remove old keyword
                # ==================
                dak_var = self.get_value_by_path(var, var_path)
                model_method = getattr(self, method_name)
                if len(path_and_model_method) == 3:
                    model = model_method(path_and_model_method[2])
                else:
                    model = model_method()
                for keyword in model:
                    if keyword in dak_var:
                        del dak_var[keyword]

                # add new keyword
                # ===============
                dak_var[value] = ''
                var.writeFile()
                self.signal(file_name, var_path, value)
            except:
                raise KeyError('Could not set sample type')

    def dakota_keyword_signal_name(self, path=None):
        if path is not None:
            file_name, _ = self.split_path(path)
            # self.debug("fv "+file_name)  # TODO: check why we get paths like 0
            return file_name
        else:
            return None

    # Check if a keyword exists in file
    # =================================
    def dakota_keyword_exists(self, path):
        if path is None:
            return False
        file_name, var_path = self.split_path(path)
        if file_name in self.dakota_files:
            var = self.dakota_files[file_name]
            try:
                self.get_value_by_path(var, var_path) # value needs to exist
                return True
            except KeyError:
                return False
        else:
            return False

    # Create specific or remove keyword
    # =================================
    def set_invalid_or_remove_var(self, path, set_invalid):
        if set_invalid:
            self.set_dakota_var(path, "")
        else:
            self.remove_from_dict(path)

    def remove_from_dict(self, path):
        if path is None:
            return
        file_name, var_path = self.split_path(path)
        if file_name in self.dakota_files:
            var = self.dakota_files[file_name]
            var_dict = self.get_dict_by_path(var, var_path)
            for key in var_dict:
                if key == var_path[-1]:
                    del var_dict[var_path[-1]]

                    var.writeFile()
                    self.signal(file_name, var_path)
        else:
            return

    # Dakota option
    # =============
    def get_dakota_option(self, path_and_default_value):
        path = path_and_default_value[0]
        return self.dakota_keyword_exists(path)

    def set_dakota_option(self, path_and_default_value, checked):
        path = path_and_default_value[0]
        default_value = path_and_default_value[1]
        if not checked:
            self.remove_from_dict(path)
        else:
            self.set_dakota_var(path, default_value)

    def dakota_option_signal_name(self, path=None):
        return "input.in"

    # Run dakota instance
    # ===================
    def dakota_exec(self, args, stdout=None, stderr=None, cwd=None):

        # Set Environment
        # ===============
        dakota_bin_path = self.dice.settings.value(self, ['DAKOTA', 'dakota'])[:-7]
        dakota_lib_path = self.dice.settings.value(self, ['DAKOTA', 'dakota'])[:-10] + "lib"
        dakota_test_path = self.dice.settings.value(self, ['DAKOTA', 'dakota'])[:-10] + "test"
        os_dakota_ld_library_path = ":" + dakota_bin_path + ":" + dakota_lib_path
        os_dakota_path = ":" + dakota_bin_path + ":" + dakota_test_path

        try:
            os.environ['LD_LIBRARY_PATH'] += os_dakota_ld_library_path
        except KeyError:
            os.environ['LD_LIBRARY_PATH'] = os_dakota_ld_library_path
        try:
            os.environ['PATH'] += os_dakota_path
        except KeyError:
            os.environ['PATH'] = os_dakota_path
        f_args = [self.dice.settings.value(self, ['DAKOTA', 'dakota'])]
        f_args.extend(args)
        cwd = self.current_run_path()
        result = self.run_process(f_args, stdout=stdout, stderr=stderr, cwd=cwd, env=os.environ)
        return result
