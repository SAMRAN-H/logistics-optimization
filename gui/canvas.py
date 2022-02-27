from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.pyplot import figure
from core import plot_curve


class Canvas(FigureCanvasQTAgg):
    def __init__(self, size=(20, 20)) -> None:
        self.figure = figure(figsize=size)
        self.axis = self.figure.add_subplot(111)
        super().__init__(self.figure)

    def plot_curve(self, alpha, beta, left, right, color):
        self.axis.cla()
        plot_curve(self.axis, alpha, beta, left, right, color)
        self.figure.canvas.draw_idle()
        self.figure.tight_layout()
