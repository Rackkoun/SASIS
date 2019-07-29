"""
Created on 23.07.2019 at 20:20
@author: Ruphus

idea source: book: python programming gui cookbook
matplolib officiel: https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
https://datatofish.com/matplotlib-charts-tkinter-gui/
"""
from tkinter.ttk import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SGraphTK:
    """
    Diese Klasse ist fuer die Einbettung von Matplolib-Darstellungen in einem
    TKinter-Rahmen zustaendig.

    Daten, die von dieser Klassen geplot werden, sind Daten, welche noch keine
    mit irgendwelchem Machinellen Lernen Algorithmus trainiert sind
    """

    def __init__(self, root=None):
        """
        Die Klasse besitzt ein Hauptframe für graphische Ansichte (gmaster) und ein inneres Frame (intern_frame_up),
        wobei, das innere Frame für die Visualisierung nicht trainierten Daten zuständig ist.
        :param root: Frame, in welchem der Graph geplot wird
        """
        self.gmaster = Frame(master=root)                  # Hauptframe: wird von einer anderen Klasse (Frame) bestimmt
        self.intern_frame = Frame(master=self.gmaster)     # innere Frame für einzelnen Graphen
        self.intern_frame.pack(side='top')
        self.gmaster.pack()

    def on_draw_line(self, x, y, xlab, ylab, lincolor, linstyle):
        """
        ...
        :param x:
        :param y:
        :param xlab:
        :param ylab:
        :param lincolor:
        :param linstyle:
        :param figcol:
        :return:
        """
        fig = plt.Figure(figsize=(4.4, 2.7), dpi=80, facecolor='white', constrained_layout=True)
        ax = fig.add_subplot(111)
        # ax = self.on_create_fig(figcol)
        ax.plot(x, y, color=lincolor, linestyle=linstyle)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)

        canvas = FigureCanvasTkAgg(fig, self.intern_frame)
        canvas.get_tk_widget().pack(side='left', padx=8)

        self.gmaster.update()
