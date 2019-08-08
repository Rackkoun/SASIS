"""
Created on 07.08.2019 at 00:07
@author: Ruphus
"""

import time
from tkinter import INSERT, WORD, END
from tkinter.scrolledtext import ScrolledText as scrollT
from tkinter.ttk import Frame, LabelFrame, Label
from gui.button.sbutton import SASISActionButton as sbutton

from database.postgresdb import PostgreSQLDatabase as DB
from model.managedata.ingeneering import DataProcessing
from model.objects.message_box import MessageTip

class DatabaseContent:

    def __init__(self, root):
        self.master = Frame(master=root)
        self.labelframe = None
        self.btn = None

        self.thread = None

        self.db_max = None
        self.db_min = None
        self.db_current = None

        self.text_field = None
        self.field_width = 40
        self.field_height = 10

        self.data_ing = DataProcessing()
        self.db = DB()
        self.config_file = './res/config/dbconfig.ini'


    def on_create_labelframe(self, name, col, row, px, py, pos):
        self.labelframe = LabelFrame(master=self.master, text=name)
        self.labelframe.grid(column=col, row=row, padx=px, pady=py, sticky=pos)

    def add_btn(self, col, row, colpad, rowpad):
        self.btn = sbutton(root=self.labelframe).get_btn()
        self.btn.configure(text='Load Content')
        self.btn.configure(command=self.on_writing_in_the_field)
        MessageTip(gui=self.btn, msg='Click here to pull the db')
        self.btn.grid(column=col, row=row, padx=rowpad, pady=colpad, sticky='W')

    def on_create_label(self, label_name, col, row, colpad, rowpad, pos):
        lab = Label(master=self.labelframe, text=label_name)
        lab.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky=pos)

    def on_create_field(self, col, row, px, py, cspan):
        self.text_field = scrollT(master=self.labelframe, width=self.field_width, height=self.field_height, wrap=WORD)
        self.text_field.grid(column=col, row=row, padx=px, pady=py, columnspan=cspan)

    def on_writing_in_the_field(self):
        if self.btn['text'] == 'Load Content':
            self.btn.configure(text='Loading...')
            self.btn.configure(bg='#ffa500')

            print(self.btn['text'], self.btn['state'])

            self.write_all()
            #self.btn.bind('<Button-1>', self.thred_text(self.btn['text']))
        time.sleep(.5)

        self.btn.configure(text='Load Content')
        self.btn.configure(bg='#00bfff')

    def format_date(self, d):
        return d.strftime('%Y %b %d')

    def write_all(self):
        print('Inhalt der Datenbank( aktuell ): \n')
        self.text_field.get(1.0, END)
        print('Inhalt nicht leer, wird gelöscht...')
        self.text_field.delete(1.0, END)

        connection = self.db.in_connecting(self.config_file)
        df = self.db.read_db_content(connection)
        id = df['id'].values
        strom = df['strom'].values
        datum = df['datum'].values
        m = df.min()
        print("MIN IN DF: ", m['strom'], "   date: ", m['datum'])

        print("STATISTIK:")
        self.print_db_stats(df)
        for i, s, d in zip(id, strom, datum):
            self.text_field.insert(INSERT, '   ' + str(i) + '\t\t' + str(s) + "\t    " + str(
                self.format_date(d)) + '\n')
            print(i, "\t", s, "\t", d)
        time.sleep(.2)

    def print_db_stats(self, df):
        new_df = self.data_ing.on_getting_data_from_server(df)
        min, max, current = new_df.min(), new_df.max(), self.data_ing.select_current_value(new_df)

        df_min = new_df[new_df['strom'] == min['strom']]
        df_max = new_df[new_df['strom'] == max['strom']]

        text1 = ' {} Watt \t\t Datum:   {}, den {}   {}   {}'.format(df_min['strom'][0], df_min['wochentag'][0],
                                                                     df_min['tag'][0], df_min.index[0].strftime('%b'),
                                                                     df_min['jahr'][0])

        text2 = ' {} Watt \t\t Datum:   {}, den {}   {}   {}'.format(df_max['strom'][0], df_max['wochentag'][0],
                                                                     df_max['tag'][0], df_max.index[0].strftime('%b'),
                                                                     df_max['jahr'][0])

        text3 = ' {} Watt \t\t Datum:   {}, den {}   {}   {}'.format(current['strom'][0], current['wochentag'][0],
                                                                     current['tag'][0], current.index[0].strftime('%b'),
                                                                     current['jahr'][0])
        self.db_min = Label(master=self.labelframe, text=text1)
        self.db_min.grid(column=3, row=0, padx=8, pady=8, sticky='N', columnspan=3)

        self.db_max = Label(master=self.labelframe, text=text2)
        self.db_max.grid(column=3, row=1, padx=8, pady=8, sticky='N', columnspan=3)

        self.db_current = Label(master=self.labelframe, text=text3)
        self.db_current.grid(column=3, row=2, padx=8, pady=8, sticky='N', columnspan=3)
    #
    # def thred_text(self, text, btn):
    #
    #     def on_refresh(event):
    #         if btn['text'] == event == 'Loading...':
    #             btn.configure(bg='#ffa500')
    #             time.sleep(.1)
    #             print(btn['text'])
    #         else:
    #             btn.configure(text='Load Content')
    #             btn.configure(bg='#00bfff')
    #             time.sleep(.1)
    #             print(btn['text'])
    #     t = Thread(target=on_refresh, args=(text, ))
    #     self.thread = t
    #     self.thread.start()
