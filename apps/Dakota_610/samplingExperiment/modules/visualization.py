"""
Visualization
=============
"""

# External modules
# ================
from bokeh.plotting import *
from PyQt5.QtCore import pyqtProperty, pyqtSlot, pyqtSignal
# from bokeh.models.renderers import GlyphRenderer
# from bokeh.embed import autoload_static
# from bokeh.resources import Resources


class Visualization:

    def __init__(self):

        self.p = []
        self.__plot_html_path = ""
        self.page_name = 'index.html'
        self.__reload_web_engine = False

        self.x1 = [0]
        self.y1 = [0]

        self.default_plot_width = 500
        self.default_plot_height = 500

    def visualization_load(self):

        self.__plot_html_path = self.config_path(self.page_name)
        output_file(self.__plot_html_path, mode="absolute")

        self.p.append(figure(plot_width=self.default_plot_width,
                         plot_height=self.default_plot_height,
                         tools="pan,wheel_zoom,box_zoom,reset,resize,previewsave"))
        self.p[0].scatter(self.x1, self.y1, size=12, color="red", alpha=0.5)
        self.p[0].toolbar_location = None

        save(HBox(self.p[0]))

    # HTML Path
    # =========
    plot_html_path_changed = pyqtSignal(name="plotHTMLPathChanged")

    @property
    def plot_html_path(self):
        return self.__plot_html_path

    @plot_html_path.setter
    def plot_html_path(self, plot_html_path):
        if self.__plot_html_path != plot_html_path:
            self.__plot_html_path = plot_html_path
            self.plot_html_path_changed.emit()

    plotHTMLPath = pyqtProperty(str, fget=plot_html_path.fget, fset=plot_html_path.fset, notify=plot_html_path_changed)

    # # Create js and tag
    # # =================
    # def create_js_tag(self):
    #     js, tag = autoload_static(self.p1, Resources(mode="absolute"), self.config_path("plot.js"))
    #     with open(self.config_path("plot.js"), "w") as file:
    #         file.write(js)
    #
    #     html_content = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Test plot</title></head><body><div id="9fe4daf9-51ec-4a04-a625-d9d6c84217a9">' + tag + '</div></body></html>'
    #     with open(self.config_path("plot.html"), "w") as file:
    #         file.write(html_content)

    # Reload plot
    # ===========
    @pyqtSlot(name="reload")
    def reload_plot(self):
        self.reload_web_engine = False
        import time
        time.sleep(0.1)
        save(vplot(self.p[0], self.p[1], self.p[2]))
        self.reload_web_engine = True

    reload_web_engine_changed = pyqtSignal(name="reloadWebEngineChanged")

    @property
    def reload_web_engine(self):
        return self.__reload_web_engine

    @reload_web_engine.setter
    def reload_web_engine(self, reload_web_engine):
        if self.__reload_web_engine != reload_web_engine:
            self.__reload_web_engine = reload_web_engine
            self.reload_web_engine_changed.emit()

    reloadWebEngine = pyqtProperty(bool, fget=reload_web_engine.fget, fset=reload_web_engine.fset, notify=reload_web_engine_changed)

    # Load data and reload plot
    # =========================
    def load_data(self, csv_data):

        self.p = []
        data = csv_data.data()
        for var_name in data:
            if var_name != "%eval_id":
                self.p.append(self.create_scatter_figure(data["%eval_id"],
                                                         data[var_name],
                                                         "i",
                                                         var_name))

        self.reload_plot()

    def create_scatter_figure(self, x, y, x_name, y_name):
        fig = figure(plot_width=self.default_plot_width,
                         plot_height=self.default_plot_height,
                         tools="pan,wheel_zoom,box_zoom,reset,resize,previewsave",
            x_axis_label=x_name,
            y_axis_label=y_name)
        fig.scatter(x, y, size=12, color="red", alpha=0.5)
        fig.toolbar_location = None

        return fig