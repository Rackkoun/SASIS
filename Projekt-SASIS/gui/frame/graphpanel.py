"""
Created on 23.07.2019 at 18:10
@author: Ruphus

"""
from tkinter import IntVar
from tkinter.ttk import Frame, LabelFrame, Label
from gui.button.sradiobutton import SASISRadioButton as rsButton
from graph.normal import SGraphTK as sgraph

import pandas as pd
from database.postgresdb import PostgreSQLDatabase as DB


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
        self.rgrp = {}  # Label fuer RadioButtons werden hier hinzugefuegt
        self.graph_up = None  # Obere Darstellung
        self.graph_down = None  # Untere Darstellung
        self.tmp = None
        self.tk_var = IntVar()

        self.config_file = './res/config/dbconfig.ini'
        self.graph_algo_dict = {}  # for tests
        self.graph_norm_dict = {}
        self.grp_frame = {}
        self.server = DB()

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
        self.lf = LabelFrame(master=self.master, text=frame_name)
        self.lf.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky=pos)

    def on_create_frame_up_lf(self, frame_name, col, row, colpad, rowpad):
        self.graph_up = LabelFrame(master=self.master, text=frame_name)
        self.graph_up.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky='NE')

        #self.graph_up = sgraph(root=self.tmp)

    def on_create_frame_down_lf(self, frame_name, col, row, colpad, rowpad):
        self.graph_down = LabelFrame(master=self.master, text=frame_name)
        self.graph_down.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky='SE')

        #self.graph_up = sgraph(root=self.tmp)

    def add_rbtn(self, algo_name, btn_value, col, row, colpad, rowpad):  # enlever le status
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
        r_btn = rsButton(root=self.lf, lname=algo_name, rad_val=btn_value, tk_int_var=self.tk_var).get_rbtn()
        r_btn.configure(state='DISABLE')
        # r_btn.configure(command=self.on_update_view_lof)

        r_btn.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky='W')
        self.set_command(algo_name, r_btn)
        self.rgrp[algo_name] = r_btn
        # self.rgrp[algo_name]['state'].bind('<Button-1>', self.on_update_view_lof(self.rgrp[algo_name]['state']))
        print("rdio state: ", self.rgrp[algo_name]['state'])

    def on_add_graph_up(self,  grp_style, col, row, px, py):
        tmp_frame = Frame(master=self.graph_up)
        tmp_frame.grid(column=col, row=row, padx=px, pady=py)
        graph = sgraph(col=col, row=row, px=px, py=py, master_lf=tmp_frame)

        print("STYLE exists")
        connection = self.server.in_connecting(self.config_file)
        df = self.server.read_db_content(connection)

        grp = df.groupby('datum')['strom'].sum()  # erzeuge ein Serie-Objekt
        reconverted_index = pd.to_datetime(grp.index)
        new_df = pd.DataFrame(grp.values, columns=['strom'], index=reconverted_index)
        new_df.index.name = None
        new_df['tag'] = new_df.index.day
        new_df['monat'] = new_df.index.month
        new_df['jahr'] = new_df.index.year
        new_df['wochentag'] = new_df.index.weekday_name
        #df = self.server.on_preprocessing_data(df)
        print(new_df)
        x = new_df['tag'].values
        y = new_df['strom'].values
        if grp_style == 'line':
            self.graph_norm_dict[grp_style] = graph
            fig = self.graph_norm_dict[grp_style].on_draw_line(x=x, y=y, xlab='Tag(in Integer)', ylab='Stromverbrauch', lincolor='r', linstyle='solid')
            self.graph_norm_dict[grp_style].put_graph_on_canvas(fig=fig)
            #self.updated_up(grp_style)
        if grp_style == 'scatter':
            self.graph_norm_dict[grp_style] = graph
            fig = self.graph_norm_dict[grp_style].on_draw_scatter(x=x, y=y, d=new_df, h=new_df['wochentag'])
            self.graph_norm_dict[grp_style].put_graph_on_canvas(fig=fig)
            #self.updated_up(grp_style)
        #if grp_style == 'box':
        #    self.graph_norm_dict[grp_style] = graph
        #    fig = self.graph_norm_dict[grp_style].on_draw_box(x=x, y=y, df=new_df, h=new_df['wochentag'])
        #    self.graph_norm_dict[grp_style].put_graph_on_canvas(fig=fig)
            #self.updated_up(grp_style)
        print(self.graph_algo_dict.keys())

    def on_add_graph_down(self, algo_name, col, row, px, py, x, y, lx, ly, c=None, s=None,):
        tmp_frame = Frame(master=self.graph_down)
        tmp_frame.grid(column=col, row=row, padx=px, pady=py)
        graph = sgraph(col=col, row=row, px=px, py=py, master_lf=tmp_frame)
        self.graph_algo_dict[algo_name] = graph
        fig = self.graph_algo_dict[algo_name].on_draw_line(x=x, y=y, xlab=lx, ylab=ly, lincolor=c, linstyle=s)
        self.graph_algo_dict[algo_name].put_graph_on_canvas(fig=fig) #
        # graph.grid(column=col, row=row, padx=px, pady=py)
        # canvas.get_tk_widget().grid(column=col, row=row, padx=px, pady=py)
        # self.graph_dict[algo_name] = canvas
        # toolbar = graph.on_update_canvas(canvas=canvas, root=self.tmp)
        # self.toolbar_dict[algo_name] = toolbar
        print(self.graph_algo_dict.keys())

    def get_panel(self):
        return self.master

    def set_command(self, algo_name, rdio_brn):
        if algo_name == 'Local Outliers Factor':
            rdio_brn.configure(command=self.on_update_view_lof)
        if algo_name == 'Isolation Forest':
            rdio_brn.configure(command=self.on_update_view_isof)

    def on_update_view_lof(self):
        if self.rgrp['Local Outliers Factor']['state'] == 'DISABLE':
            self.rgrp['Local Outliers Factor']['state'] = 'ENABLE'
            print(self.rgrp['Local Outliers Factor']['state'])
            connection = self.server.in_connecting(self.config_file)
            df = self.server.read_db_content(connection)
            print(df.head(4))
            x = df['id'].values
            y = df['strom'].values
            # tmp_frame = Frame(master=self.tmp)
            # grp = sgraph()
            fig = self.graph_algo_dict['Local Outliers Factor'].on_draw_line(x=x, y=y, xlab='ID', ylab='STROM', lincolor='r',
                                                                             linstyle='solid')
            self.graph_algo_dict['Local Outliers Factor'].on_update_canvas(fig=fig)
        else:
            self.rgrp['Local Outliers Factor']['state'] = 'DISABLE'
            print(self.rgrp['Local Outliers Factor']['state'])

    def on_update_view_isof(self):
        if self.rgrp['Isolation Forest']['state'] == 'DISABLE':
            self.rgrp['Isolation Forest']['state'] = 'ENABLE'
            print(self.rgrp['Isolation Forest']['state'])
            connection = self.server.in_connecting(self.config_file)
            df = self.server.read_db_content(connection)
            print(df.head(4))
            x = df['id'].values
            y = df['strom'].values
            # tmp_frame = Frame(master=self.tmp)
            # grp = sgraph()
            fig = self.graph_algo_dict['Isolation Forest'].on_draw_line(x=x, y=y, xlab='ID', ylab='STROM', lincolor='g',
                                                                        linstyle='solid')
            self.graph_algo_dict['Isolation Forest'].on_update_canvas(fig=fig)
        else:
            self.rgrp['Isolation Forest']['state'] = 'DISABLE'
            print(self.rgrp['Isolation Forest']['state'])
