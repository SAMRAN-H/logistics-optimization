from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.pyplot import figure
from core import set_axis_props


class Canvas(FigureCanvasQTAgg):
    def __init__(self, size=(20, 20)) -> None:
        self.figure = figure(figsize=size)
        self.axis = self.figure.add_subplot(111)
        super().__init__(self.figure)

    def plot_curve(self, plot_func, params):
        self.axis.cla()

        if type(plot_func) == list:
            for func in plot_func:
                func(self.axis, params)
        else:
            plot_func(self.axis, params)

        self.axis.legend(frameon=False)
        # self.axis.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
        #           ncol=3, frameon=False)
        set_axis_props(self.axis)

        self.figure.canvas.draw_idle()
        self.figure.tight_layout()
