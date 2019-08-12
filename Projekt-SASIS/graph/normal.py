"""
Created on 23.07.2019 at 20:20
@author: Ruphus

idea source: book: python programming gui cookbook
matplolib officiel: https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html
https://datatofish.com/matplotlib-charts-tkinter-gui/
"""
from tkinter.ttk import Frame
import matplotlib.pyplot as plt
import seaborn as sb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SGraphTK:
    """
    Diese Klasse ist fuer die Einbettung von Matplolib-Darstellungen in einem
    TKinter-Rahmen zustaendig.

    Daten, die von dieser Klassen geplot werden, sind Daten, welche noch keine
    mit irgendwelchem Machinellen Lernen Algorithmus trainiert sind
    """

    def __init__(self, col, row, px, py, master_lf=None):
        """
        Die Klasse besitzt ein Hauptframe für graphische Ansichte (gmaster) und ein inneres Frame (intern_frame_up),
        wobei, das innere Frame für die Visualisierung nicht trainierten Daten zuständig ist.
        :param root: Frame, in welchem der Graph geplot wird
        """
        self.gmaster = master_lf                 # Hauptframe: wird von einer anderen Klasse (Frame) bestimmt
        self.gmaster.grid(column=col, row=row, padx=px, pady=py)
        self.intern_frame = Frame(master=self.gmaster)     # innere Frame für einzelnen Graphen
        self.intern_frame.grid(column=col, row=row, padx=px, pady=py)

        self.canvas = None
        self.frame = None
        pass

    def on_draw_line(self, x, y, xlab, ylab, lincolor=None, linstyle=None):
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
        ax.plot(x, y, color=lincolor, linestyle=linstyle)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        ax.set_title('Täglicher Stromverbauch')

        return fig

    def put_graph_on_canvas(self, fig): #
        self.canvas = FigureCanvasTkAgg(fig, master=self.intern_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0, padx=5, pady=5)
        self.intern_frame.update()

    def on_update_canvas(self, fig):
        self.canvas = None
        self.put_graph_on_canvas(fig)

    def on_draw_scatter(self, x, y, d=None, h=None):
        fig = plt.Figure(figsize=(4.4, 2.7), dpi=80, facecolor='white', constrained_layout=True)
        ax = fig.add_subplot(111)
        sb.scatterplot(x=x, y=y, hue=h, data=d, ax=ax)
        ax.set_xlabel('Tage (in Integer)')
        ax.set_ylabel('Stromverbrauch (in w min)')
        ax.set_title('Wöchentliche Stromverbauch')

        return fig

    # https://stackoverflow.com/questions/31594549/how-do-i-change-the-figure-size-for-a-seaborn-plot
    def on_draw_box(self, x, y, df=None, h=None):
        fig = plt.Figure(figsize=(4.4, 2.7), dpi=80, facecolor='white', constrained_layout=True)
        ax = fig.add_subplot(111)
        sb.boxplot(x=x, y=y, data=df, hue=h, ax=ax)
        ax.set_xlabel('Wochentage')
        ax.set_ylabel('Stromverbrauch (in w min)')
        ax.set_title('Monatlicher Stromverbauch')
        ax.set_xticklabels(labels=x, rotation=15)

        return fig

    def on_draw_bar(self, x, y, h=None, data=None):
        """

        :param x:
        :param y:
        :param data:
        :return:
        """
        fig = plt.Figure(figsize=(4.4, 2.7), dpi=80, facecolor='white', constrained_layout=True)
        ax = fig.add_subplot(111)
        sb.catplot(x=x, y=y, hue=h, data=data, kind='bar', ax=ax)
        ax.set_xlabel('Wochentage')
        ax.set_ylabel('Stromverbrauch (in w min)')
        ax.set_title('Monatlicher Stromverbauch')
        ax.set_xticklabels(labels=x, rotation=15)

        return fig