from PyQt6 import uic, QtWidgets

from pathlib import Path
from core.core import plot_mc_and_deviation, plot_triangle_distribution, plot_analytic_triangle, plot_uniform_mc

from gui.canvas import Canvas


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, title):
        super().__init__()

        uic.loadUi(Path(__file__).parent.resolve().joinpath('ui.ui'), self)
        self.setWindowTitle(title)

        self.plot_func = [[plot_triangle_distribution, plot_analytic_triangle],
                          [plot_mc_and_deviation, plot_uniform_mc]]

        self.canvas = Canvas()
        self.tab_index = 0

        self.mean_text = ''
        self.std_text = ''

        layout = self.tab_widget.widget(0).layout()
        layout.addWidget(self.canvas)

    def on_tab_change(self, tab_index):
        previous_layout = self.tab_widget.widget(
            self.tab_index).layout()
        previous_layout.removeWidget(self.canvas)
        layout = self.tab_widget.widget(tab_index).layout()
        layout.addWidget(self.canvas)

        self.mean.setVisible(tab_index == 0)
        self.std.setVisible(tab_index == 0)

        self.tab_index = tab_index
        self.plot_curve()

    def plot_curve(self):
        left = float(self.left.text())
        right = float(self.right.text())
        alpha = float(self.alpha.text())
        beta = float(self.beta.text())
        m = float(self.m.text())
        n = float(self.n.text())
        c = int(self.c.text())

        params = {
            'alpha': alpha,
            'beta': beta,
            'left': left,
            'right': right,
            'n': n,
            'm': m,
            'c': c,
            'set_mean': self.set_mean,
            'set_std': self.set_std
        }

        self.canvas.plot_curve(self.plot_func[self.tab_index], params)

    def set_mean(self, new_mean):
        mean = self.mean.text()
        if not self.mean_text:
            self.mean_text = mean

        text = f'{self.mean_text} {new_mean:.2f}'

        self.mean.setText(text)

    def set_std(self, new_std):
        std = self.std.text()
        if not self.std_text:
            self.std_text = std

        text = f'{self.std_text} {new_std:.2f}'

        self.std.setText(text)
