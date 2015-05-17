# Standard Python modules
# =======================
import os

# External modules
# ================
from PyQt5.QtCore import pyqtProperty, pyqtSlot, pyqtSignal, qDebug

# DICE modules
# ============
from core.dice.core_app import CoreApp
from core.dice.tools.json_sync import JsonOrderedDict


class Settings(CoreApp):
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)

        self.__settings_tree = [
            {
                'text': 'OpenFOAM'
            },
            {
                'text': 'ParaView'
            },
            {
                'text': 'DAKOTA'
            }]

        settings_folder = os.path.join(os.path.expanduser("~"), ".config", "DICE")
        if not os.path.exists(settings_folder):
            os.makedirs(settings_folder)

        self.__settings = JsonOrderedDict(os.path.join(settings_folder, "settings.json"))
        self.__load_default_if_empty_settings()

    settings_tree_changed = pyqtSignal(name="settings_treeChanged")

    @property
    def settings_tree(self):
        return self.__settings_tree

    @settings_tree.setter
    def settings_tree(self, settings_tree):
        if self.__settings_tree != settings_tree:
            self.__settings_tree = settings_tree
            self.settings_tree_changed.emit()

    settingsTree = pyqtProperty("QVariantList", fget=settings_tree.fget, fset=settings_tree.fset,
                                notify=settings_tree_changed)

    @pyqtSlot("QStringList", name="settingsList", result="QVariantList")
    def settings_list(self, settings_path):
        """
        Gets a path to a selected setting as a list of strings and returns all parameters that can be set for it.
        :param settings_path:
        :return:
        """
        for app_name in self.__settings:
            if app_name == settings_path[0]:
                for label, value in self.__settings[app_name].items():
                    return [
                        {
                            'label': label,
                            'value': value
                        }
                    ]

    @pyqtSlot("QStringList", str, "QVariant", name="setValue")
    def set_value(self, path, label, value):
        app_name = path[0]
        if app_name in self.__settings:
            self.__settings[app_name][label] = value
            self.__settings.write()
            self.settings_tree_changed.emit()

    def value(self, app, settings_path):
        try:
            return self.__settings[settings_path[0]][settings_path[1]]
        except KeyError:
            return None

    def __load_default_if_empty_settings(self):
        if self.__settings == {}:
            self.__settings['OpenFOAM'] = {'foamExec': 'foamExec'}
            self.__settings['ParaView'] = {'paraview': 'paraview'}
            self.__settings['DAKOTA'] = {'dakota': 'dakota'}