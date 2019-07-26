"""
Created on 23.07.2019 at 18:10
@author: Ruphus

"""

from tkinter.ttk import Frame, LabelFrame, Label
from gui.button.sradiobutton import SASISRadioButton as rsButton
from graph.normal import SGraphTK as sgraph


class MonitorringControl:
    """
    Dieser Klasse steuert sowohl RadioButton als auch Graphen in dem Reiter fuer die Graphenansicht
    """

    def __init__(self, root):
        """

        :param root: Frame in dem Canvas- und RadioButton-Elementen gepackt werden
        """
        self.master = Frame(master=root)
        self.lf = None  # Labelframe fuer die Hierarchie der Elementen
        self.rgrp = []  # Label fuer RadioButtons werden hier hinzugefuegt
        self.graph_up = None  # Obere Darstellung
        self.graph_down = None  # Untere Darstellung
        self.tmp = None

    def on_create_labelframe(self, frame_name, col, row, colpad, rowpad, pos):
        """
        Erstellung eines oberen Bezeichner fuer ein Element und Positionierung des Elements in einem Frame
        :param frame_name: Titel oben auf ein Objekt
        :param col: Spalten
        :param row: ZEile
        :param colpad: Innenabstand in der Spaltenrichtung
        :param rowpad: Innenabstand in der Zeilenrichtung
        :param pos: Plazierung in einem Frame ('N':Nord, 'S':Sued, 'W':West, usw.)
        :return:
        """
        self.lf = LabelFrame(master=self.master, \
                             text=frame_name)
        self.lf.grid(column=col, row=row, padx=colpad, \
                     pady=rowpad, sticky=pos)

    def on_create_glabelframe(self, frame_name, col, row, colpad, rowpad, pos):
        self.tmp = LabelFrame(master=self.master, \
                             text=frame_name)
        self.tmp.grid(column=col, row=row, padx=colpad, \
                     pady=rowpad, sticky=pos)

        self.graph_up = sgraph(root=self.tmp)

    def add_rbtn(self, name, btn_value, col, row, colpad, rowpad, tk_var=None):  # enlever le status
        """
        Erzeugung eines RadioButtons und Plazierung des Buttons in einem Frame
        :param name: Name des Bezeichner neben fuer den RadioButton
        :param btn_value: Werte des RadioButtons (Dieser Werte wird im Verbindung mit einer TK-Variable gebraucht)
        :param col:  Spalte fuer die Positionierung des RadioButtons
        :param row: Zeile fuer die Positionierung des RadioButtons
        :param colpad: Innenabstand des RadioButton in der Spaltenrichtung
        :param rowpad: Innenabstand des RadioButtons in der Zeilenrichtung
        :param tk_var: TKinter-Variable fuer den Aufruf des Wertes eines RadioButtons
        :return:
        """
        r_btn = rsButton(root=self.lf, name=name, rad_val=btn_value, tk_int_var=tk_var)
        r_btn.set_btn_pos(col, row, colpad, rowpad)
        self.rgrp.append(r_btn)

    def onDraw(self, x, y, lx, ly, c, s):
        self.graph_up.on_draw_line(x=x, y=y, xlab=lx, ylab=ly, lincolor=c, linstyle=s)

    def get_panel(self):
        return self.master
