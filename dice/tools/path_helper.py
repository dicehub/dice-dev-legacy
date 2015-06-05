import os


class PathHelper():

    def module_abspath(self):
        # doesn't work as a property, we need it during construction
        return os.path.abspath(os.path.join(*self.__module__.split(".")[:-1]))

    def module_path(self, *sub_paths):
        return os.path.join(self.module_abspath(), *sub_paths)
