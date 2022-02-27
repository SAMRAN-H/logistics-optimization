from PyQt6 import uic, QtWidgets

from pathlib import Path

from gui.canvas import Canvas


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, title):
        super().__init__()

        uic.loadUi(Path(__file__).parent.resolve().joinpath('ui.ui'), self)
        self.setWindowTitle(title)

        self.canvas = Canvas()
        self.render_figure()

    def render_figure(self):
        layout = self.placeholder.parent().layout()
        layout.replaceWidget(self.placeholder, self.canvas)

    def plot_curve(self):
        left = float(self.left.text())
        right = float(self.right.text())
        alpha = float(self.alpha.text())
        beta = float(self.beta.text())

        self.canvas.plot_curve(alpha, beta, left, right, 'blue')
