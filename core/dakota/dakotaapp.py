# DICE modules
# ============
from core.app import BasicApp


class DakotaApp(BasicApp):
    app_name = "NoNameDakotaApp"

    def __init__(self, parent, instance_name, status):
        BasicApp.__init__(self, parent, instance_name, status)

        self.dakota_files = dict()

    # def register_dakota_file(self, path, var):