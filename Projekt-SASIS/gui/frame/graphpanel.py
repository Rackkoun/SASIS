"""
Created on 23.07.2019 at 18:10
@author: Ruphus

"""
from tkinter import IntVar
from tkinter.ttk import Frame, LabelFrame
from gui.button.sradiobutton import SASISRadioButton as rsButton
from graph.normal import SGraphTK as sgraph
from graph.predictions import SGraphMLTK as mlgraph

import pandas as pd
import numpy as np
from database.postgresdb import PostgreSQLDatabase as DB

from model.algorithms.onclass import OneCSVM
from model.algorithms.elliptic import EllipticEnv
from model.algorithms.factor import LocOuFac
from model.algorithms.forest import IsolFo

from model.managedata.testdata import TestDataGenerator
from model.managedata.ingeneering import DataProcessing


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
        self.graph_algo_dict = {}
        self.graph_norm_dict = {}
        self.grp_frame = {}
        self.server = DB()

        self.data = {}
        self.data_ing = DataProcessing()
        self.model_one = OneCSVM()
        self.model_isof = IsolFo()
        self.model_ellipenv = EllipticEnv()
        self.model_lof = LocOuFac()

        self.train_all_modell()  # trainiere alla Model für zukünftige Vorhersage

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

    def on_create_frame_down_lf(self, frame_name, col, row, colpad, rowpad):
        self.graph_down = LabelFrame(master=self.master, text=frame_name)
        self.graph_down.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky='SE')

    def add_rbtn(self, algo_name, btn_value, col, row, colpad, rowpad):  # enlever le status
        """

        :param algo_name:
        :param btn_value:
        :param col:
        :param row:
        :param colpad:
        :param rowpad:
        :return:
        """
        r_btn = rsButton(root=self.lf, lname=algo_name, rad_val=btn_value, tk_int_var=self.tk_var).get_rbtn()
        r_btn.configure(state='DISABLE')

        r_btn.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky='W')
        self.set_command(algo_name, r_btn)
        self.rgrp[algo_name] = r_btn

        print("rdio state: ", self.rgrp[algo_name]['state'])

    def on_add_graph_up(self, grp_style, col, row, px, py):
        tmp_frame = Frame(master=self.graph_up)
        tmp_frame.grid(column=col, row=row, padx=px, pady=py)
        graph = sgraph(col=col, row=row, px=px, py=py, master_lf=tmp_frame)

        print("STYLE exists")
        connection = self.server.in_connecting(self.config_file)
        df = self.server.read_db_content(connection)

        grp = df.groupby('datum')['strom'].sum()  # erzeuge ein Serie-Objekt
        print(grp.values)
        reconverted_index = pd.to_datetime(grp.index)
        new_df = pd.DataFrame(grp.values, columns=['strom'], dtype=np.float, index=reconverted_index)
        new_df.index.name = None
        new_df['tag'] = new_df.index.day
        new_df['monat'] = new_df.index.month
        new_df['jahr'] = new_df.index.year
        new_df['wochentag'] = new_df.index.weekday_name

        print(new_df)
        x = new_df['tag'].values
        y = new_df['strom'].values
        yb = new_df['strom'].values.tolist()
        print("Y: ", y, 'type: ', y.dtype)  # , '\nyf: ', yf, 'type: ', yf.dtype)
        print("Y: ", yb, 'type: ', type(yb))
        xb = new_df['wochentag']
        hb = new_df['monat']
        if grp_style == 'line':
            self.graph_norm_dict[grp_style] = graph
            fig = self.graph_norm_dict[grp_style].on_draw_line(x=df['id'], y=df['strom'], xlab='ID (In Integer)',
                                                               ylab='Stromverbrauch (in w min)', linstyle='solid',
                                                               lincolor='r')
            self.graph_norm_dict[grp_style].put_graph_on_canvas(fig=fig)
        if grp_style == 'scatter':
            self.graph_norm_dict[grp_style] = graph
            fig = self.graph_norm_dict[grp_style].on_draw_scatter(x=x, y=y, d=new_df, h=new_df['wochentag'])
            self.graph_norm_dict[grp_style].put_graph_on_canvas(fig=fig)
        if grp_style == 'box':
            self.graph_norm_dict[grp_style] = graph
            fig = self.graph_norm_dict[grp_style].on_draw_box(x=xb, y=yb, df=new_df, h=hb)
            self.graph_norm_dict[grp_style].put_graph_on_canvas(fig=fig)
        if grp_style == 'hist':
            self.graph_norm_dict[grp_style] = graph
            fig = self.graph_norm_dict[grp_style].on_draw_hist(x=xb, y=y, data=df)
            self.graph_norm_dict[grp_style].put_graph_on_canvas(fig=fig)
        print(self.graph_algo_dict.keys())

    def on_add_graph_down(self, algo_name, col, row, px, py, x, y, x1=None, y1=None, x2=None, y2=None, pred=None):
        tmp_frame = Frame(master=self.graph_down)
        tmp_frame.grid(column=col, row=row, padx=px, pady=py)
        graph = mlgraph(col=col, row=row, px=px, py=py, master_lf=tmp_frame)
        self.graph_algo_dict[algo_name] = graph
        fig = self.graph_algo_dict[algo_name].draw(x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2, pred=pred)
        self.graph_algo_dict[algo_name].put_graph_on_canvas(fig=fig)
        print(self.graph_algo_dict.keys())

    def get_panel(self):
        return self.master

    def set_command(self, algo_name, rdio_brn):
        if algo_name == 'Local Outliers Factor':
            rdio_brn.configure(command=self.on_update_view_lof)
        if algo_name == 'Isolation Forest':
            rdio_brn.configure(command=self.on_update_view_isof)
        if algo_name == 'Elliptic Envelope':
            rdio_brn.configure(command=self.on_update_view_ellenv)
        if algo_name == 'One Class SVM':
            rdio_brn.configure(command=self.on_update_view_oncsvm)

    def on_update_view_lof(self):
        if self.rgrp['Local Outliers Factor']['state'] == 'DISABLE':
            self.rgrp['Local Outliers Factor']['state'] = 'ENABLE'
            print(self.rgrp['Local Outliers Factor']['state'])

            connection = self.server.in_connecting(self.config_file)  # erstelle eine Verbindung zum Server
            df = self.server.read_db_content(connection)  # rufe date vom Server ab
            print("GROBE DATEN VOM SERVER:\n", df.head(4))

            df2 = self.data_ing.on_getting_data_from_server(df)  # gruppiere die Daten in einem DF
            print("DATEN nach der Gruppierung: \n", df2)

            X = self.data_ing.split_for_sasis(df2)  # Wandle die in 2D-NP-Array
            x_pred = self.model_lof.predict_locoufac(X)  # mache eine Vorhersage
            print("Prediction: ", x_pred)

            self.data['Local Outliers Factor'] = self.data_ing.on_predictinng_new_value(X[:, 0], x_pred, self.data[
                'Local Outliers Factor'])
            x = self.data['Local Outliers Factor']['tag'].values
            y = self.data['Local Outliers Factor']['strom'].values
            print("Value in DF: \n", self.data['Local Outliers Factor'].tail(3))

            outliers = self.data_ing.detect_outliers(self.data['Local Outliers Factor'])
            x1 = outliers.tag.values
            y1 = outliers.strom.values
            print("Outliers:\n", outliers)

            current_use = self.data_ing.select_current_value(self.data['Local Outliers Factor'])
            x2 = current_use['tag'].values
            y2 = current_use['strom'].values
            print("Heutige Verbrauch:\n", current_use)

            fig = self.graph_algo_dict['Local Outliers Factor'].draw(x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2, pred=x_pred,
                                                                     algo_name='Local Outliers Factor')
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
            print("GROBE DATEN VOM SERVER:\n", df.head(4))

            df2 = self.data_ing.on_getting_data_from_server(df)
            print("DATEN nach der Gruppierung: \n", df2)

            X = self.data_ing.split_for_sasis(df2)
            x_pred = self.model_isof.predict_isolfo(X)
            print("Prediction: ", x_pred)

            self.data['Isolation Forest'] = self.data_ing.on_predictinng_new_value(X[:, 0], x_pred, self.data[
                'Isolation Forest'])
            x = self.data['Isolation Forest']['tag'].values
            y = self.data['Isolation Forest']['strom'].values
            print("Value in DF: \n", self.data['Isolation Forest'].tail(3))

            outliers = self.data_ing.detect_outliers(self.data['Isolation Forest'])
            x1 = outliers.tag.values
            y1 = outliers.strom.values
            print("Outliers:\n", outliers)

            current_use = self.data_ing.select_current_value(self.data['Isolation Forest'])
            x2 = current_use['tag'].values
            y2 = current_use['strom'].values
            print("Heutige Verbrauch:\n", current_use)

            fig = self.graph_algo_dict['Isolation Forest'].draw(x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2, pred=x_pred,
                                                                algo_name='Isolation Forest')
            self.graph_algo_dict['Isolation Forest'].on_update_canvas(fig=fig)
        else:
            self.rgrp['Isolation Forest']['state'] = 'DISABLE'
            print(self.rgrp['Isolation Forest']['state'])

    def on_update_view_ellenv(self):
        if self.rgrp['Elliptic Envelope']['state'] == 'DISABLE':
            self.rgrp['Elliptic Envelope']['state'] = 'ENABLE'
            print(self.rgrp['Elliptic Envelope']['state'])

            connection = self.server.in_connecting(self.config_file)
            df = self.server.read_db_content(connection)
            print("GROBE DATEN VOM SERVER:\n", df.head(4))

            df2 = self.data_ing.on_getting_data_from_server(df)
            print("DATEN nach der Gruppierung: \n", df2)

            X = self.data_ing.split_for_sasis(df2)
            x_pred = self.model_ellipenv.predict_ellipenv(X)
            print("Prediction: ", x_pred)

            self.data['Elliptic Envelope'] = self.data_ing.on_predictinng_new_value(X[:, 0], x_pred, self.data[
                'Elliptic Envelope'])
            x = self.data['Elliptic Envelope']['tag'].values
            y = self.data['Elliptic Envelope']['strom'].values
            print("Value in DF: \n", self.data['Elliptic Envelope'].tail(3))

            outliers = self.data_ing.detect_outliers(self.data['Elliptic Envelope'])
            x1 = outliers.tag.values
            y1 = outliers.strom.values
            print("Outliers:\n", outliers)

            current_use = self.data_ing.select_current_value(self.data['Elliptic Envelope'])
            x2 = current_use['tag'].values
            y2 = current_use['strom'].values
            print("Heutige Verbrauch:\n", current_use)

            fig = self.graph_algo_dict['Elliptic Envelope'].draw(x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2, pred=x_pred,
                                                                 algo_name='Isolation Forest')
            self.graph_algo_dict['Elliptic Envelope'].on_update_canvas(fig=fig)
        else:
            self.rgrp['Elliptic Envelope']['state'] = 'DISABLE'
            print(self.rgrp['Elliptic Envelope']['state'])

    def on_update_view_oncsvm(self):
        if self.rgrp['One Class SVM']['state'] == 'DISABLE':
            self.rgrp['One Class SVM']['state'] = 'ENABLE'
            print(self.rgrp['One Class SVM']['state'])

            connection = self.server.in_connecting(self.config_file)
            df = self.server.read_db_content(connection)
            print("GROBE DATEN VOM SERVER:\n", df.head(4))

            df2 = self.data_ing.on_getting_data_from_server(df)
            print("DATEN nach der Gruppierung: \n", df2)

            X = self.data_ing.split_for_sasis(df2)
            x_pred = self.model_one.predict_one_csvm(X)
            print("Prediction: ", x_pred)

            self.data['One Class SVM'] = self.data_ing.on_predictinng_new_value(X[:, 0], x_pred, self.data[
                'One Class SVM'])
            x = self.data['One Class SVM']['tag'].values
            y = self.data['One Class SVM']['strom'].values
            print("Value in DF: \n", self.data['One Class SVM'].tail(3))

            outliers = self.data_ing.detect_outliers(self.data['One Class SVM'])
            x1 = outliers.tag.values
            y1 = outliers.strom.values
            print("Outliers:\n", outliers)

            current_use = self.data_ing.select_current_value(self.data['One Class SVM'])
            x2 = current_use['tag'].values
            y2 = current_use['strom'].values
            print("Heutige Verbrauch:\n", current_use)

            fig = self.graph_algo_dict['One Class SVM'].draw(x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2, pred=x_pred,
                                                             algo_name='Isolation Forest')
            self.graph_algo_dict['One Class SVM'].on_update_canvas(fig=fig)
        else:
            self.rgrp['One Class SVM']['state'] = 'DISABLE'
            print(self.rgrp['One Class SVM']['state'])

    def train_all_modell(self):
        test = TestDataGenerator()
        tmp_df = test.make_quick_gen()             # generiere Test daten
        X = self.data_ing.split_for_sasis(tmp_df)  # wähle die zu trainierenden Spalten daraus
                                                   # trainiere die mit allen Algorithmen
        self.model_ellipenv.train_ellipenv(X)
        self.model_isof.train_isolfo(X)
        self.model_lof.train_locoufac(X)
        self.model_one.train_one_csvm(X)
                                                    # dann probiere eine kleine Vorhersage damit
                                                    # (Normalerweise nicht empfohlen)
        epred = self.model_ellipenv.predict_ellipenv(X)
        ipred = self.model_isof.predict_isolfo(X)
        lpred = self.model_lof.predict_locoufac(X)
        opred = self.model_one.predict_one_csvm(X)
                                                     # füge eine neue Spalte hinzu,
                                                     # welche die vorhergesagenen Daten erhält
        self.data['Elliptic Envelope'] = self.data_ing.after_trainig_data(tmp_df, epred)
        self.data['Isolation Forest'] = self.data_ing.after_trainig_data(tmp_df, ipred)
        self.data['Local Outliers Factor'] = self.data_ing.after_trainig_data(tmp_df, lpred)
        self.data['One Class SVM'] = self.data_ing.after_trainig_data(tmp_df, opred)
