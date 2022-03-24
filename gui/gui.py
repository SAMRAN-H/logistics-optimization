from PyQt6 import uic, QtWidgets, QtCore

from pathlib import Path
from core.core import plot_mc_and_deviation, plot_triangle_distribution, plot_analytic_triangle

from gui.canvas import Canvas


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, title):
        super().__init__()

        uic.loadUi(Path(__file__).parent.resolve().joinpath('ui.ui'), self)
        self.setWindowTitle(title)

        self.plot_func = [[plot_triangle_distribution, plot_analytic_triangle],
                          plot_mc_and_deviation]

        self.canvas = Canvas()
        self.tab_index = 0

        layout = self.tab_widget.widget(0).layout()
        layout.addWidget(self.canvas)

    def on_tab_change(self, tab_index):
        previous_layout = self.tab_widget.widget(
            self.tab_index).layout()
        previous_layout.removeWidget(self.canvas)
        layout = self.tab_widget.widget(tab_index).layout()
        layout.addWidget(self.canvas)
        self.tab_index = tab_index
        self.plot_curve()

    def plot_curve(self):
        left = float(self.left.text())
        right = float(self.right.text())
        alpha = float(self.alpha.text())
        beta = float(self.beta.text())
        m = float(self.m.text())
        n = float(self.n.text())

        params = {
            'alpha': alpha,
            'beta': beta,
            'left': left,
            'right': right,
            'n': n,
            'm': m
        }

        self.canvas.plot_curve(self.plot_func[self.tab_index], params)
