"""
Created on 05.08.2019 at 19:22
@author: Ruphus
"""
from tkinter.ttk import Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SGraphMLTK:
    """
        Diese Klasse steht für die Darstellung trinierter Daten. Die Methoden ähneln sich von
        dieser in dem Module normal.py, aber sie werden noch mehrere Optionsparameter anbieten
        """

    def __init__(self, col, row, px, py, master_lf=None):
        """

        :param col:
        :param row:
        :param px:
        :param py:
        :param master_lf:
        """
        self.gmaster = master_lf  # Hauptframe: wird von einer anderen Klasse (Frame) bestimmt
        self.gmaster.grid(column=col, row=row, padx=px, pady=py)
        self.intern_frame = Frame(master=self.gmaster)  # innere Frame für einzelnen Graphen
        self.intern_frame.grid(column=col, row=row, padx=px, pady=py)

        self.canvas = None
        self.frame = None
        pass

    def draw(self, x, y, x1=None, y1=None, x2=None, y2=None, pred=None, algo_name=None):
        """

        :param x:
        :param y:
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :param pred:
        :param algo_name:
        :return: fig
        """
        fig = plt.Figure(figsize=(4.4, 2.7), dpi=80, facecolor='white', constrained_layout=True)
        ax = fig.add_subplot(111)
        ax.scatter(x=x, y=y, c='white', edgecolors='k', label='Stromverbrauch')
        ax.scatter(x=x1, y=y1, c='red', label='Outliers')
        if pred == -1:
            ax.scatter(x=x2, y=y2, c='red', s=100, label='Neuer Eintrag')
        else:
            ax.scatter(x=x2, y=y2, c='green', s=80, label='Neuer Eintrag')

        ax.set_xlabel('Tage (in Integer)')
        ax.set_ylabel('Stromverbrauch (in w min)')
        ax.set_title(algo_name)
        ax.legend(loc='best')

        return fig

    def put_graph_on_canvas(self, fig):  #
        self.canvas = FigureCanvasTkAgg(fig, master=self.intern_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, padx=5, pady=5)
        self.intern_frame.update()

    def on_update_canvas(self, fig):
        self.canvas = None
        self.put_graph_on_canvas(fig)
