import os.path
import numpy as np
from tkinter import IntVar
import time
from threading import Thread
from queue import Queue
from tkinter.ttk import Frame, LabelFrame, Label
from PIL import Image, ImageTk
from gui.button.sbutton import SASISActionButton as sButton
from model.elementdict.labelmodel import LabelModel
from model.constants.pictures import HousePlan

"""@author: Ruphus
   Created on 20.07.2019
   source: Threading: https://automatetheboringstuff.com/chapter15/
                   https://www.devdungeon.com/content/gui-programming-python#threads 
"""


class ApplianceDeviceControl:
    """ Diese Klasse ist fuer die Darstellung von Steuerelemente fuer den Strom verantwortlich
    z. B.: Lichte, Waschmaschine, Fernseher. usw."""

    def __init__(self, root):
        """

        :param root:
        """
        self.dev_control_panel = Frame(master=root)
        self.panel_control_lf = None
        self.house_plan_lf = None
        self.house_lbl = None
        self.filepath = './res/img/'
        self.plan = HousePlan().load_plan

        self.thread_dict = {}
        self.queue = Queue()
        self.dict_btn = {}
        self.dict_tk_var = {}

        # self.dev_control_panel.update()
        pass

    def get_panel(self):
        return self.dev_control_panel

    ##########################################################################
    #      Methoden für die Positionierung von Sichten auf dem Frame         #
    ##########################################################################
    def on_adding_basic_appliance(self, lname, col, row, px, py, pos):
        self.create_new_intern_label(label_name=lname, col=col, row=row, colpad=px, rowpad=py, pos=pos)
        self.add_btn(col=col + 1, row=row, px=px, py=py, room_name=lname)

    def add_btn(self, col, row, px, py, room_name):
        btn = sButton(root=self.panel_control_lf).get_btn()
        self.set_btn_command(room_name=room_name, btn=btn)
        btn.grid(column=col, row=row, padx=px, pady=py)

        tk_var = IntVar()
        self.dict_btn[room_name] = btn
        self.dict_tk_var[room_name] = tk_var

        print("Raum: ", room_name, " - - > Button STATE: ", self.dict_btn[room_name]['state'], " - - > TK Var Wert: ",
              self.dict_tk_var[room_name].get())

    def create_new_intern_label(self, label_name, col, row, colpad, rowpad, pos):
        mlab = LabelModel(label_name)
        mlab.obj = Label(master=self.panel_control_lf, text=mlab.name)
        mlab.obj.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky=pos)

    def on_create_labelframe(self, frame_name, col, row, colpad, rowpad, pos, pic=None):

        if pic == None:

            self.panel_control_lf = LabelFrame(master=self.dev_control_panel, text=frame_name)
            self.panel_control_lf.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky=pos)
        else:
            self.house_plan_lf = LabelFrame(master=self.dev_control_panel, text=frame_name)
            self.house_plan_lf.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky=pos)
            img = None
            try:
                img = Image.open(os.path.join(self.filepath, str(self.plan[pic])))
                print(str(self.plan[pic]))
            except IOError:
                pass

            print(img.mode, '- - - - ', img.size)
            img.rotate(90)                              # Bild Umdrehen
            img.thumbnail((884, 400), Image.ANTIALIAS)  # groesse des Bild anpassen
            img_lbl = ImageTk.PhotoImage(image=img)     # ohne dass --> UnboundLocalError: local variable 'img'

            # referenced before assignment img_lbl musst als label image zugewiesen werden
            # ohne dass - - > _tkinter.TclError: image specification must contain an odd number of elements
            self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
            self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
            self.house_lbl = img_lbl  # und diese Zuweisung am Ende

    #############################################################################################
    #                                Verwaltung von Bilder                                      #
    #############################################################################################

    def set_btn_command(self, room_name, btn):
        if room_name == 'WZ':
            btn.configure(command=self.on_updated_00)
        if room_name == 'SZ':
            btn.configure(command=self.on_updated_01)
        if room_name == 'WC':
            btn.configure(command=self.on_updated_02)
        if room_name == 'DUSCHE':
            btn.configure(command=self.on_updated_03)
        if room_name == 'WZ + K':
            btn.configure(command=self.on_updated_04)
        if room_name == 'WZ + K + KP4':
            btn.configure(command=self.on_updated_05)
        if room_name == 'WZ + K + WM4':
            btn.configure(command=self.on_updated_06)
        if room_name == 'WZ + K + KP4 + WM4':
            btn.configure(command=self.on_updated_07)
        if room_name == 'ALLE LICHTER EIN':
            btn.configure(command=self.on_updated_08)
        if room_name == 'ALLE LICHTER AUS':
            btn.configure(command=self.on_updated_09)

    def on_updated_action(self, btn_obj_name):
        """

        :param btn_obj_name:
        :return:
        """
        try:
            img = Image.open(os.path.join(self.filepath, self.plan[btn_obj_name]))

            img.rotate(90)
            img.thumbnail((884, 400), Image.ANTIALIAS)
            img_lbl = ImageTk.PhotoImage(image=img)
            self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
            self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
            self.house_lbl = img_lbl
        except IOError as ierror:
            print('Fehler beim Laden des Bildes: -->', ierror)
        except KeyError as kerror:
            print('Variable nicht erkannt: --> ', kerror)

    def on_updated_00(self):
        if self.dict_btn['WZ']['text'] == 'OFF': # prüfen den aktuellen Text im Button
            self.dict_btn['WZ']['text'] = 'ON'   # dann ändere ihn mit dem hier
            self.dict_btn['WZ'].configure(state='ON') # dasselbe auch für den Button-Zustand
            print(self.dict_btn['WZ']['state'])
            self.on_updated_action('WZ')             # rufe die Methode für dementsprechenden Raumname auf

            # und setze eine Verbindung zwischen dem Button und der Methode auf, welche in einem Thread läuft
            self.dict_btn['WZ'].bind('<Button-1>', self.on_thread_00(self.dict_btn['WZ']['state']))

        else:
            self.dict_btn['WZ']['text'] = 'OFF' # sonst setze den Text
            self.dict_btn['WZ']['state'] = 'OFF' # und Button-Zustand in dem vorherigen Zustand zurück
            print("Last values of Va-00 = ", self.dict_tk_var['WZ'].get()) # prüfe der gepeicherte Wert in der TK-Var

            try: # setzte das Bild auch auf dem ersten Zustand zurück
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['WZ']['state'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

            print("STATE OF THR IN DICT: ", self.thread_dict['WZ'].is_alive())
            if self.thread_dict['WZ'].is_alive(): # der Thread ist noch am Leben
                self.thread_dict['WZ'].join(.25) # versuche ihn abzuschliessen
                print("STATS OF DICT NOW: ", self.thread_dict['WZ'].is_alive())
                dauer = self.dict_tk_var['WZ'].get() # der letzte Wert in der TK-Var in temporärer Var speichern
                print("STORED VALUE: ", dauer)
                print("REINIT TKVAT: ")
                self.dict_tk_var['WZ'].set(0) # der TK-Var auf 0 zurücksetzen
                print("TK VAR REINIT TO: ", self.dict_tk_var['WZ'].get())
                print("STATS OF DICT NOW 2: ", self.thread_dict['WZ'].is_alive())
                print("VERBRAUCH IN WZ: ", np.round((dauer * 2.), decimals=2), "watt min") # der Verbrauch in der DB speichern

    def on_updated_01(self):
        if self.dict_btn['SZ']['text'] == 'OFF':
            self.dict_btn['SZ']['text'] = 'ON'
            self.dict_btn['SZ'].configure(state='ON')
            print(self.dict_btn['SZ']['state'])
            self.on_updated_action('SZ')
            self.dict_btn['SZ'].bind('<Button-1>', self.on_thread_01(self.dict_btn['SZ']['state']))
        else:
            self.dict_btn['SZ']['text'] = 'OFF'
            self.dict_btn['SZ']['state'] = 'OFF'
            print("Last values of Va-01 = ", self.dict_tk_var['SZ'].get())

            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['SZ']['state'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

            if self.thread_dict['SZ'].is_alive():
                self.thread_dict['SZ'].join(.25)
                print("STATS OF DICT NOW: ", self.thread_dict['SZ'].is_alive())
                dauer = self.dict_tk_var['SZ'].get()
                print("STORED VALUE: ", dauer)
                print("REINIT TKVAT: ")
                self.dict_tk_var['SZ'].set(0)
                print("TK VAR REINIT TO: ", self.dict_tk_var['SZ'].get())
                print("STATS OF DICT NOW 2: ", self.thread_dict['SZ'].is_alive())
                print("VERBRAUCH IN SZ: ", np.round((dauer * 1.), decimals=2), "watt min")

    def on_updated_02(self):
        if self.dict_btn['WC']['text'] == 'OFF':
            self.dict_btn['WC']['text'] = 'ON'
            self.dict_btn['WC'].configure(state='ON')
            print(self.dict_btn['WC']['state'])
            self.on_updated_action('WC')
            self.dict_btn['WC'].bind('<Button-1>', self.on_thread_02(self.dict_btn['WC']['state']))
        else:
            self.dict_btn['WC']['text'] = 'OFF'
            self.dict_btn['WC']['state'] = 'OFF'
            print("Last values of Va-02 = ", self.dict_tk_var['WC'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['WC']['text'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

            if self.thread_dict['WC'].is_alive():
                self.thread_dict['WC'].join(.25)
                print("STATS OF DICT NOW: ", self.thread_dict['WC'].is_alive())
                dauer = self.dict_tk_var['WC'].get()
                print("STORED VALUE: ", dauer)
                print("REINIT TKVAT: ")
                self.dict_tk_var['WC'].set(0)
                print("TK VAR REINIT TO: ", self.dict_tk_var['WC'].get())
                print("STATS OF DICT NOW 2: ", self.thread_dict['WC'].is_alive())
                print("VERBRAUCH IN WC: ", np.round((dauer * 1.), decimals=2), "watt min")

    def on_updated_03(self):
        if self.dict_btn['DUSCHE']['text'] == 'OFF':
            self.dict_btn['DUSCHE']['text'] = 'ON'
            self.dict_btn['DUSCHE'].configure(state='ON')
            print(self.dict_btn['DUSCHE']['state'])
            self.on_updated_action('DUSCHE')
            self.dict_btn['DUSCHE'].bind('<Button-1>', self.on_thread_03(self.dict_btn['DUSCHE']['state']))
        else:
            self.dict_btn['DUSCHE']['text'] = 'OFF'
            self.dict_btn['DUSCHE']['state'] = 'OFF'
            print("Last values of Va-03 = ", self.dict_tk_var['DUSCHE'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['DUSCHE']['state'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

            if self.thread_dict['DUSCHE'].is_alive():
                self.thread_dict['DUSCHE'].join(.25)
                print("STATS OF DICT NOW: ", self.thread_dict['DUSCHE'].is_alive())
                dauer = self.dict_tk_var['DUSCHE'].get()
                print("STORED VALUE: ", dauer)
                print("REINIT TKVAT: ")
                self.dict_tk_var['DUSCHE'].set(0)
                print("TK VAR REINIT TO: ", self.dict_tk_var['DUSCHE'].get())
                print("STATS OF DICT NOW 2: ", self.thread_dict['DUSCHE'].is_alive())
                print("VERBRAUCH IN DUSCHE: ", np.round((dauer * 1.), decimals=2), "watt min")

    def on_updated_04(self):
        if self.dict_btn['WZ + K']['text'] == 'OFF':
            self.dict_btn['WZ + K']['text'] = 'ON'
            self.dict_btn['WZ + K'].configure(state='ON')
            print(self.dict_btn['WZ + K']['state'])
            self.on_updated_action('WZ + K')
            self.dict_btn['WZ + K'].bind('<Button-1>', self.on_thread_04(self.dict_btn['WZ + K']['state']))
        else:
            self.dict_btn['WZ + K']['text'] = 'OFF'
            self.dict_btn['WZ + K']['state'] = 'OFF'
            print("Last values of Va-04 = ", self.dict_tk_var['WZ + K'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['WZ + K']['state'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

            if self.thread_dict['WZ + K'].is_alive():
                self.thread_dict['WZ + K'].join(.25)
                print("STATS OF DICT NOW: ", self.thread_dict['WZ + K'].is_alive())
                dauer = self.dict_tk_var['WZ + K'].get()
                print("STORED VALUE: ", dauer)
                print("REINIT TKVAT: ")
                self.dict_tk_var['WZ + K'].set(0)
                print("TK VAR REINIT TO: ", self.dict_tk_var['WZ + K'].get())
                print("STATS OF DICT NOW 2: ", self.thread_dict['WZ + K'].is_alive())
                print("VERBRAUCH IN WZ + K: ", np.round((dauer * 2.), decimals=2), "watt min")

    def on_updated_05(self):
        if self.dict_btn['WZ + K + KP4']['text'] == 'OFF':
            self.dict_btn['WZ + K + KP4']['text'] = 'ON'
            self.dict_btn['WZ + K + KP4'].configure(state='ON')
            print(self.dict_btn['WZ + K + KP4']['state'])
            self.on_updated_action('WZ + K + KP4')
            self.dict_btn['WZ + K + KP4'].bind('<Button-1>', self.on_thread_05(self.dict_btn['WZ + K + KP4']['state']))
        else:
            self.dict_btn['WZ + K + KP4']['text'] = 'OFF'
            self.dict_btn['WZ + K + KP4']['state'] = 'OFF'
            print("Last values of Va-05 = ", self.dict_tk_var['WZ + K + KP4'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['WZ + K + KP4']['text'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

            if self.thread_dict['WZ + K + KP4'].is_alive():
                self.thread_dict['WZ + K + KP4'].join(.25)
                print("STATS OF DICT NOW: ", self.thread_dict['WZ + K + KP4'].is_alive())
                dauer = self.dict_tk_var['WZ + K + KP4'].get()
                print("STORED VALUE: ", dauer)
                print("REINIT TKVAT: ")
                self.dict_tk_var['WZ + K + KP4'].set(0)
                print("TK VAR REINIT TO: ", self.dict_tk_var['WZ + K + KP4'].get())
                print("STATS OF DICT NOW 2: ", self.thread_dict['WZ + K + KP4'].is_alive())
                print("VERBRAUCH IN WZ + K + KP4: ", np.round((dauer * 68.67), decimals=2), "watt min") # 1+1+66,67 watt min

    def on_updated_06(self):
        if self.dict_btn['WZ + K + WM4']['text'] == 'OFF':
            self.dict_btn['WZ + K + WM4']['text'] = 'ON'
            self.dict_btn['WZ + K + WM4'].configure(state='ON')
            print(self.dict_btn['WZ + K + WM4']['state'])
            self.on_updated_action('WZ + K + WM4')
            self.dict_btn['WZ + K + WM4'].bind('<Button-1>', self.on_thread_06(self.dict_btn['WZ + K + WM4']['state']))
        else:
            self.dict_btn['WZ + K + WM4']['text'] = 'OFF'
            self.dict_btn['WZ + K + WM4']['state'] = 'OFF'
            print("Last values of Va-06 = ", self.dict_tk_var['WZ + K + WM4'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['WZ + K + WM4']['text'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

            if self.thread_dict['WZ + K + WM4'].is_alive():
                self.thread_dict['WZ + K + WM4'].join(.25)
                print("STATS OF DICT NOW: ", self.thread_dict['WZ + K + WM4'].is_alive())
                dauer = self.dict_tk_var['WZ + K + WM4'].get()
                print("STORED VALUE: ", dauer)
                print("REINIT TKVAT: ")
                self.dict_tk_var['WZ + K + WM4'].set(0)
                print("TK VAR REINIT TO: ", self.dict_tk_var['WZ + K + WM4'].get())
                print("STATS OF DICT NOW 2: ", self.thread_dict['WZ + K + WM4'].is_alive())
                print("VERBRAUCH IN WZ + K + WM4: ", np.round((dauer * 38.67), decimals=2), "watt min") # 1+1+66,67 watt min

    def on_updated_07(self):
        if self.dict_btn['WZ + K + KP4 + WM4']['text'] == 'OFF':
            self.dict_btn['WZ + K + KP4 + WM4']['text'] = 'ON'
            self.dict_btn['WZ + K + KP4 + WM4'].configure(state='ON')
            print(self.dict_btn['WZ + K + KP4 + WM4']['state'])
            self.on_updated_action('WZ + K + KP4 + WM4')
            self.dict_btn['WZ + K + KP4 + WM4'].bind('<Button-1>',
                                                     self.on_thread_07(self.dict_btn['WZ + K + KP4 + WM4']['state']))
        else:
            self.dict_btn['WZ + K + KP4 + WM4']['text'] = 'OFF'
            self.dict_btn['WZ + K + KP4 + WM4']['state'] = 'OFF'
            print("Last values of Va-07 = ", self.dict_tk_var['WZ + K + KP4 + WM4'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['WZ + K + KP4 + WM4']['text'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

            if self.thread_dict['WZ + K + KP4 + WM4'].is_alive():
                self.thread_dict['WZ + K + KP4 + WM4'].join(.25)
                print("STATS OF DICT NOW: ", self.thread_dict['WZ + K + KP4 + WM4'].is_alive())
                dauer = self.dict_tk_var['WZ + K + KP4 + WM4'].get()
                print("STORED VALUE: ", dauer)
                print("REINIT TKVAT: ")
                self.dict_tk_var['WZ + K + KP4 + WM4'].set(0)
                print("TK VAR REINIT TO: ", self.dict_tk_var['WZ + K + KP4 + WM4'].get())
                print("STATS OF DICT NOW 2: ", self.thread_dict['WZ + K + KP4 + WM4'].is_alive())
                print("VERBRAUCH IN WZ + K + KP4 + WM4: ", np.round((dauer * 105.34), decimals=2), "watt min") # 1+1+66,67+36,67 watt min

    def on_updated_08(self):
        if self.dict_btn['ALLE LICHTER EIN']['text'] == 'OFF':
            self.dict_btn['ALLE LICHTER EIN']['text'] = 'ON'
            self.dict_btn['ALLE LICHTER EIN'].configure(state='ON')
            print(self.dict_btn['ALLE LICHTER EIN']['state'])
            self.on_updated_action('ALLE LICHTER EIN')
            self.dict_btn['ALLE LICHTER EIN'].bind('<Button-1>', self.on_thread_08(self.dict_btn['ALLE LICHTER EIN']['state']))
        else:
            self.dict_btn['ALLE LICHTER EIN']['text'] = 'OFF'
            self.dict_btn['ALLE LICHTER EIN']['state'] = 'OFF'
            print("Last values of Va-08 = ", self.dict_tk_var['ALLE LICHTER EIN'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['ALLE LICHTER EIN']['text'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

            if self.thread_dict['ALLE LICHTER EIN'].is_alive():
                self.thread_dict['ALLE LICHTER EIN'].join(.25)
                print("STATS OF DICT NOW: ", self.thread_dict['ALLE LICHTER EIN'].is_alive())
                dauer = self.dict_tk_var['ALLE LICHTER EIN'].get()
                print("STORED VALUE: ", dauer)
                print("REINIT TKVAT: ")
                self.dict_tk_var['ALLE LICHTER EIN'].set(0)
                print("TK VAR REINIT TO: ", self.dict_tk_var['ALLE LICHTER EIN'].get())
                print("STATS OF DICT NOW 2: ", self.thread_dict['ALLE LICHTER EIN'].is_alive())
                print("VERBRAUCH IN ALLE LICHTER EIN: ", np.round((dauer * 9.), decimals=2), "watt min")

    def on_updated_09(self):
        if self.dict_btn['ALLE LICHTER AUS']['text'] == 'OFF':
            self.dict_btn['ALLE LICHTER AUS']['text'] = 'ON'
            self.dict_btn['ALLE LICHTER AUS'].configure(state='ON')
            print(self.dict_btn['ALLE LICHTER AUS']['state'])
            self.on_updated_action('ALLE LICHTER AUS')
            self.dict_btn['ALLE LICHTER AUS'].bind('<Button-1>', self.on_thread_09(self.dict_btn['ALLE LICHTER AUS']['state']))
        else:
            self.dict_btn['ALLE LICHTER AUS']['text'] = 'OFF'
            self.dict_btn['ALLE LICHTER AUS']['state'] = 'OFF'
            print("Last values of Va-09 = ", self.dict_tk_var['ALLE LICHTER AUS'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['ALLE LICHTER AUS']['text'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

            if self.thread_dict['ALLE LICHTER AUS'].is_alive():
                self.thread_dict['ALLE LICHTER AUS'].join(.25)
                print("STATS OF DICT NOW: ", self.thread_dict['ALLE LICHTER AUS'].is_alive())
                dauer = self.dict_tk_var['ALLE LICHTER AUS'].get()
                print("STORED VALUE: ", dauer)
                print("REINIT TKVAT: ")
                self.dict_tk_var['ALLE LICHTER AUS'].set(0)
                print("TK VAR REINIT TO: ", self.dict_tk_var['ALLE LICHTER AUS'].get())
                print("STATS OF DICT NOW 2: ", self.thread_dict['ALLE LICHTER AUS'].is_alive())
                print("VERBRAUCH IN ALLE LICHTER AUS: ", np.round((dauer * 1.), decimals=2), "watt min")

    def on_updated_10(self):
        if self.dict_btn['NICHST']['text'] == 'OFF':
            self.dict_btn['NICHST']['text'] = 'ON'
            self.dict_btn['NICHST'].configure(state='ON')
            print(self.dict_btn['NICHST']['state'])
            self.on_updated_action('NICHST')
            self.dict_btn['NICHST'].bind('<Button-1>', self.on_thread_10(self.dict_btn['NICHST']['state']))
        else:
            self.dict_btn['NICHST']['text'] = 'OFF'
            self.dict_btn['NICHST']['state'] = 'OFF'
            print("Last values of Va-10 = ", self.dict_tk_var['NICHST'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['NICHST']['text'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

    ## Multi-Threading: https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
    ## https://stackoverflow.com/questions/41711357/python-how-to-multi-thread-a-function-that-returns-multiple-values
    ## https://stackoverflow.com/questions/11986005/better-way-to-get-results-from-multiple-threads
    ## Thread: https://nitratine.net/blog/post/python-threading-basics/
    def on_inc00(self, state):
        while self.dict_btn['WZ']['state'] == state == 'ON':
            self.dict_tk_var['WZ'].set(self.dict_tk_var['WZ'].get() + 1)  # für die Inkrementierung
            self.queue.put(self.dict_tk_var['WZ'].get())  # Werte in der Warteschlage hinterlegen
            print('WZ', ":  values - - > ", self.dict_tk_var['WZ'].get())
            print("value in Q0: ", self.queue.get())  # für die IPC
            time.sleep(2)

    def on_thread_00(self, state):
        t00 = Thread(target=self.on_inc00, args=(state,))
        self.thread_dict['WZ'] = t00  # Thread in der Liste hinzufügen
        print("Thread 00 (", t00.getName(), "): added in List- - -> State: ", t00.isAlive())
        print("Thread_dict 00 (", self.thread_dict['WZ'].getName(), "): added in List- - -> State: ",
              self.thread_dict['WZ'].isAlive())
        t00.start()

    def on_inc01(self, state):
        while self.dict_btn['SZ']['state'] == state == 'ON':
            self.dict_tk_var['SZ'].set(self.dict_tk_var['SZ'].get() + 1)
            self.queue.put(self.dict_tk_var['SZ'].get())
            print('SZ', ":  values - - > ", self.dict_tk_var['SZ'].get())
            print("Value in Q1: ", self.queue.get())
            time.sleep(2)

    def on_thread_01(self, state):
        t01 = Thread(target=self.on_inc01, args=(state,))
        self.thread_dict['SZ'] = t01  # Thread in der Liste hinzufügen
        print("Thread 01 (", t01.getName(), "): added in List- - -> State: ", t01.isAlive())
        print("Thread_dict 01 (", self.thread_dict['SZ'].getName(), "): added in List- - -> State: ",
              self.thread_dict['SZ'].isAlive())
        t01.start()

    def on_inc02(self, state):
        while self.dict_btn['WC']['state'] == state == 'ON':
            self.dict_tk_var['WC'].set(self.dict_tk_var['WC'].get() + 1)
            print('WC', ":  values - - > ", self.dict_tk_var['WC'].get())
            time.sleep(2)

    def on_thread_02(self, state):
        t02 = Thread(target=self.on_inc02, args=(state,))
        self.thread_dict['WC'] = t02  # Thread in der Liste hinzufügen
        print("Thread 02 (", t02.getName(), "): added in List- - -> State: ", t02.isAlive())
        print("Thread_dict 02 (", self.thread_dict['WC'].getName(), "): added in List- - -> State: ",
              self.thread_dict['WC'].isAlive())
        t02.start()

    def on_inc03(self, state):
        while self.dict_btn['DUSCHE']['state'] == state == 'ON':
            self.dict_tk_var['DUSCHE'].set(self.dict_tk_var['DUSCHE'].get() + 1)
            print('DUSCHE', ":  values - - > ", self.dict_tk_var['DUSCHE'].get())
            time.sleep(2)

    def on_thread_03(self, state):
        t03 = Thread(target=self.on_inc03, args=(state,))
        self.thread_dict['DUSCHE'] = t03  # Thread in der Liste hinzufügen
        print("Thread 03 (", t03.getName(), "): added in List- - -> State: ", t03.isAlive())
        print("Thread_dict 03 (", self.thread_dict['DUSCHE'].getName(), "): added in List- - -> State: ",
              self.thread_dict['DUSCHE'].isAlive())
        t03.start()

    def on_inc04(self, state):
        while self.dict_btn['WZ + K']['state'] == state == 'ON':
            self.dict_tk_var['WZ + K'].set(self.dict_tk_var['WZ + K'].get() + 1)
            print('WZ + K', ":  values - - > ", self.dict_tk_var['WZ + K'].get())
            time.sleep(2)

    def on_thread_04(self, state):
        t04 = Thread(target=self.on_inc04, args=(state,))
        self.thread_dict['WZ + K'] = t04  # Thread in der Liste hinzufügen
        print("Thread 04 (", t04.getName(), "): added in List- - -> State: ", t04.isAlive())
        print("Thread_dict 04 (", self.thread_dict['WZ + K'].getName(), "): added in List- - -> State: ",
              self.thread_dict['WZ + K'].isAlive())
        t04.start()

    def on_inc05(self, state):
        while self.dict_btn['WZ + K + KP4']['state'] == state == 'ON':
            self.dict_tk_var['WZ + K + KP4'].set(self.dict_tk_var['WZ + K + KP4'].get() + 1)
            print('WZ + K + KP4', ":  values - - > ", self.dict_tk_var['WZ + k + KP4'].get())
            time.sleep(2)

    def on_thread_05(self, state):
        t05 = Thread(target=self.on_inc05, args=(state,))
        self.thread_dict['WZ + K + KP4'] = t05  # Thread in der Liste hinzufügen
        print("Thread 05 (", t05.getName(), "): added in List- - -> State: ", t05.isAlive())
        print("Thread_dict 05 (", self.thread_dict['WZ + K + KP4'].getName(), "): added in List- - -> State: ",
              self.thread_dict['WZ + K + KP4'].isAlive())
        t05.start()

    def on_inc06(self, state):
        while self.dict_btn['WZ + K + WM4']['state'] == state == 'ON':
            self.dict_tk_var['WZ + K + WM4'].set(self.dict_tk_var['WZ + K + WM4'].get() + 1)
            print('WZ + K + WM4', ":  values - - > ", self.dict_tk_var['WZ + K + WM4'].get())
            time.sleep(2)

    def on_thread_06(self, state):
        t06 = Thread(target=self.on_inc06, args=(state,))
        self.thread_dict['WZ + K + WM4'] = t06  # Thread in der Liste hinzufügen
        print("Thread 06 (", t06.getName(), "): added in List- - -> State: ", t06.isAlive())
        print("Thread_dict 06 (", self.thread_dict['WZ + K + WM4'].getName(), "): added in List- - -> State: ",
              self.thread_dict['WZ + K + WM4'].isAlive())
        t06.start()

    def on_inc07(self, state):
        while self.dict_btn['WZ + K + KP4 + WM4']['state'] == state == 'ON':
            self.dict_tk_var['WZ + K + KP4 + WM4'].set(self.dict_tk_var['WZ + K + KP4 + WM4'].get() + 1)
            print('WZ + K + KP4 + WM4', ":  values - - > ", self.dict_tk_var['WZ + K + KP4 + WM4'].get())
            time.sleep(2)

    def on_thread_07(self, state):
        t07 = Thread(target=self.on_inc07, args=(state,))
        self.thread_dict['WZ + K + KP4 + WM4'] = t07  # Thread in der Liste hinzufügen
        print("Thread 07 (", t07.getName(), "): added in List- - -> State: ", t07.isAlive())
        print("Thread_dict 07 (", self.thread_dict['WZ + K + KP4 + WM4'].getName(), "): added in List- - -> State: ",
              self.thread_dict['WZ + K + KP4 + WM4'].isAlive())
        t07.start()

    def on_inc08(self, state):
        while self.dict_btn['ALLE LICHTER EIN']['state'] == state == 'ON':
            self.dict_tk_var['ALLE LICHTER EIN'].set(self.dict_tk_var['ALLE LICHTER EIN'].get() + 1)
            print('ALLE LICHTER EIN', ":  values - - > ", self.dict_tk_var['ALLE LICHTER EIN'].get())
            time.sleep(2)

    def on_thread_08(self, state):
        t08 = Thread(target=self.on_inc08, args=(state,))
        self.thread_dict['ALLE LICHTER EIN'] = t08  # Thread in der Liste hinzufügen
        print("Thread 08 (", t08.getName(), "): added in List- - -> State: ", t08.isAlive())
        print("Thread_dict 08 (", self.thread_dict['ALLE LICHTER EIN'].getName(), "): added in List- - -> State: ",
              self.thread_dict['ALLE LICHTER EIN'].isAlive())
        t08.start()

    def on_inc09(self, state):
        while self.dict_btn['ALLE LICHTER AUS']['state'] == state == 'ON':
            self.dict_tk_var['ALLE LICHTER AUS'].set(self.dict_tk_var['ALLE LICHTER AUS'].get() + 1)
            print('ALLE LICHTER AUS', ":  values - - > ", self.dict_tk_var['ALLE LICHTER AUS'].get())
            time.sleep(2)

    def on_thread_09(self, state):
        t09 = Thread(target=self.on_inc09, args=(state,))
        self.thread_dict['ALLE LICHTER AUS'] = t09  # Thread in der Liste hinzufügen
        print("Thread 09 (", t09.getName(), "): added in List- - -> State: ", t09.isAlive())
        print("Thread_dict 09 (", self.thread_dict['ALLE LICHTER AUS'].getName(), "): added in List- - -> State: ",
              self.thread_dict['ALLE LICHTER AUS'].isAlive())
        t09.start()

    def on_inc10(self, state):
        while self.dict_btn['NICHST']['state'] == state == 'ON':
            self.dict_tk_var['NICHST'].set(self.dict_tk_var['NICHST'].get() + 1)
            print('NICHST', ":  values - - > ", self.dict_tk_var['NICHST'].get())
            time.sleep(2)

    def on_thread_10(self, state):
        t10 = Thread(target=self.on_inc10, args=(state,))
        t10.start()

    def get_all_tk_value(self):
        pass
