import os.path
from tkinter import IntVar
import time
from threading import Thread
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

        self.dict_btn = {}
        self.dict_tk_var = {}
        pass

    def get_panel(self):
        return self.dev_control_panel

    ##########################################################################
    #      Methoden für die Positionierung von Sichten auf dem Frame         #
    ##########################################################################
    def on_adding_basic_appliance(self, lname, col, row, px, py, pos):
        self.create_new_intern_label(label_name=lname, col=col, row=row, colpad=px, rowpad=py, pos=pos)
        self.add_btn(col=col + 1, row=row, px=px, py=py, room_name=lname)

        for a, b in zip(self.dict_btn.keys(), self.dict_btn.values()):
            print("room name: ", a, "--> State: ", b['state'])

        self.show_all_tk_var()

    def add_btn(self, col, row, px, py, room_name):
        btn = sButton(root=self.panel_control_lf).get_btn()
        self.set_btn_command(room_name=room_name, btn=btn)
        btn.grid(column=col, row=row, padx=px, pady=py)
        tk_var = IntVar()
        self.dict_btn[room_name] = btn
        self.dict_tk_var[room_name] = tk_var

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
            img.rotate(90)
            img.thumbnail((884, 400), Image.ANTIALIAS)  # groesse des Bild anpassen
            img_lbl = ImageTk.PhotoImage(image=img)  # ohne dass --> UnboundLocalError: local variable 'img'
            # referenced before assignment
            self.house_lbl = Label(self.house_plan_lf,
                                   image=img_lbl)  ## ohne dass - - > _tkinter.TclError: image specification must contain an odd number of elements
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
        if room_name == 'ALLES EIN':
            btn.configure(command=self.on_updated_08)
        if room_name == 'ALLES AUS':
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
            img_lbl = ImageTk.PhotoImage(
                image=img)  # ohne dass --> UnboundLocalError: local variable 'img' referenced before assignment
            self.house_lbl = Label(self.house_plan_lf,
                                   image=img_lbl)  ## ohne dass - - > _tkinter.TclError: image specification must contain an odd number of elements
            self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
            self.house_lbl = img_lbl  # und diese Zuweisung am Ende
        except IOError as ierror:
            print('Fehler beim Laden des Bildes: -->', ierror)
        except KeyError as kerror:
            print('Variable nicht erkannt: --> ', kerror)

    def on_updated_00(self):
        if self.dict_btn['WZ']['text'] == 'OFF':
            self.dict_btn['WZ']['text'] = 'ON'
            self.dict_btn['WZ'].configure(state='ON')
            print(self.dict_btn['WZ']['state'])
            self.on_updated_action('WZ')
            self.dict_btn['WZ'].bind('<Button-1>', self.on_thread_00(self.dict_btn['WZ']['state']))
        else:
            self.dict_btn['WZ']['text'] = 'OFF'
            self.dict_btn['WZ']['state'] = 'OFF'
            print("Last values of Va0 = ", self.dict_tk_var['WZ'].get())
            try:
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
            print("Last values of Va1 = ", self.dict_tk_var['SZ'].get())
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
            print("Last values of Va2 = ", self.dict_tk_var['WC'].get())
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
            print("Last values of Va3 = ", self.dict_tk_var['DUSCHE'].get())
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
            print("Last values of Va4 = ", self.dict_tk_var['WZ + K'].get())
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
            print("Last values of Va5 = ", self.dict_tk_var['WZ + K + KP4'].get())
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
            print("Last values of Va6 = ", self.dict_tk_var['WZ + K + WM4'].get())
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
            print("Last values of Va7 = ", self.dict_tk_var['WZ + K + KP4 + WM4'].get())
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

    def on_updated_08(self):
        if self.dict_btn['ALLES EIN']['text'] == 'OFF':
            self.dict_btn['ALLES EIN']['text'] = 'ON'
            self.dict_btn['ALLES EIN'].configure(state='ON')
            print(self.dict_btn['ALLES EIN']['state'])
            self.on_updated_action('ALLES EIN')
            self.dict_btn['ALLES EIN'].bind('<Button-1>', self.on_thread_08(self.dict_btn['ALLES EIN']['state']))
        else:
            self.dict_btn['ALLES EIN']['text'] = 'OFF'
            self.dict_btn['ALLES EIN']['state'] = 'OFF'
            print("Last values of Va0 = ", self.dict_tk_var['ALLES EIN'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['ALLES EIN']['text'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

    def on_updated_09(self):
        if self.dict_btn['ALLES AUS']['text'] == 'OFF':
            self.dict_btn['ALLES AUS']['text'] = 'ON'
            self.dict_btn['ALLES AUS'].configure(state='ON')
            print(self.dict_btn['ALLES AUS']['state'])
            self.on_updated_action('ALLES AUS')
            self.dict_btn['ALLES AUS'].bind('<Button-1>', self.on_thread_09(self.dict_btn['ALLES AUS']['state']))
        else:
            self.dict_btn['ALLES AUS']['text'] = 'OFF'
            self.dict_btn['ALLES AUS']['state'] = 'OFF'
            print("Last values of Va9 = ", self.dict_tk_var['ALLES AUS'].get())
            try:
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                img_lbl = ImageTk.PhotoImage(
                    image=img)
                self.house_lbl = Label(self.house_plan_lf, image=img_lbl)
                self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
                self.house_lbl = img_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.dict_btn['ALLES AUS']['text'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

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
            print("Last values of Va10 = ", self.dict_tk_var['NICHST'].get())
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

    def on_inc00(self, state):
        while self.dict_btn['WZ']['state'] == state == 'ON':
            self.dict_tk_var['WZ'].set(self.dict_tk_var['WZ'].get() + 1)

            print('WZ', ":  values - - > ", self.dict_tk_var['WZ'].get())
            time.sleep(2)

    def on_thread_00(self, state):
        t00 = Thread(target=self.on_inc00, args=(state,))
        t00.start()

    def on_inc01(self, state):
        while self.dict_btn['SZ']['state'] == state == 'ON':
            self.dict_tk_var['SZ'].set(self.dict_tk_var['SZ'].get() + 1)

            print('SZ', ":  values - - > ", self.dict_tk_var['SZ'].get())
            time.sleep(2)

    def on_thread_01(self, state):
        t01 = Thread(target=self.on_inc01, args=(state,))
        t01.start()

    def on_inc02(self, state):
        while self.dict_btn['WC']['state'] == state == 'ON':
            self.dict_tk_var['WC'].set(self.dict_tk_var['WC'].get() + 1)

            print('WC', ":  values - - > ", self.dict_tk_var['WC'].get())
            time.sleep(2)

    def on_thread_02(self, state):
        t02 = Thread(target=self.on_inc02, args=(state,))
        t02.start()

    def on_inc03(self, state):
        while self.dict_btn['DUSCHE']['state'] == state == 'ON':
            self.dict_tk_var['DUSCHE'].set(self.dict_tk_var['DUSCHE'].get() + 1)

            print('DUSCHE', ":  values - - > ", self.dict_tk_var['DUSCHE'].get())
            time.sleep(2)

    def on_thread_03(self, state):
        t03 = Thread(target=self.on_inc03, args=(state,))
        t03.start()

    def on_inc04(self, state):
        while self.dict_btn['WZ + K']['state'] == state == 'ON':
            self.dict_tk_var['WZ + K'].set(self.dict_tk_var['WZ + K'].get() + 1)

            print('WZ + K', ":  values - - > ", self.dict_tk_var['WZ + K'].get())
            time.sleep(2)

    def on_thread_04(self, state):
        t04 = Thread(target=self.on_inc04, args=(state,))
        t04.start()

    def on_inc05(self, state):
        while self.dict_btn['WZ + K +KP4']['state'] == state == 'ON':
            self.dict_tk_var['WZ + K + KP4'].set(self.dict_tk_var['WZ + K +KP4'].get() + 1)

            print('WZ + K + KP4', ":  values - - > ", self.dict_tk_var['WZ + k + KP4'].get())
            time.sleep(2)

    def on_thread_05(self, state):
        t05 = Thread(target=self.on_inc05, args=(state,))
        t05.start()

    def on_inc06(self, state):
        while self.dict_btn['WZ + K + WM4']['state'] == state == 'ON':
            self.dict_tk_var['WZ + K + WM4'].set(self.dict_tk_var['WZ + K + WM4'].get() + 1)

            print('WZ + K + WM4', ":  values - - > ", self.dict_tk_var['WZ + K + WM4'].get())
            time.sleep(2)

    def on_thread_06(self, state):
        t06 = Thread(target=self.on_inc06, args=(state,))
        t06.start()

    def on_inc07(self, state):
        while self.dict_btn['WZ + K + KP4 + WM4']['state'] == state == 'ON':
            self.dict_tk_var['WZ + K + KP4 + WM4'].set(self.dict_tk_var['WZ + K + KP4 + WM4'].get() + 1)

            print('WZ + K + KP4 + WM4', ":  values - - > ", self.dict_tk_var['WZ + K + KP4 + WM4'].get())
            time.sleep(2)

    def on_thread_07(self, state):
        t07 = Thread(target=self.on_inc07, args=(state,))
        t07.start()

    def on_inc08(self, state):
        while self.dict_btn['ALLES EIN']['state'] == state == 'ON':
            self.dict_tk_var['ALLES EIN'].set(self.dict_tk_var['ALLES EIN'].get() + 1)

            print('ALLES EIN', ":  values - - > ", self.dict_tk_var['ALLES EIN'].get())
            time.sleep(2)

    def on_thread_08(self, state):
        t08 = Thread(target=self.on_inc08, args=(state,))
        t08.start()

    def on_inc09(self, state):
        while self.dict_btn['ALLES AUS']['state'] == state == 'ON':
            self.dict_tk_var['ALLES AUS'].set(self.dict_tk_var['ALLES AUS'].get() + 1)

            print('ALLES AUS', ":  values - - > ", self.dict_tk_var['ALLES AUS'].get())
            time.sleep(2)

    def on_thread_09(self, state):
        t09 = Thread(target=self.on_inc09, args=(state,))
        t09.start()

    def on_inc10(self, state):
        while self.dict_btn['NICHST']['state'] == state == 'ON':
            self.dict_tk_var['NICHST'].set(self.dict_tk_var['NICHST'].get() + 1)

            print('NICHST', ":  values - - > ", self.dict_tk_var['NICHST'].get())
            time.sleep(2)

    def on_thread_10(self, state):
        t10 = Thread(target=self.on_inc10, args=(state,))
        t10.start()

    def show_all_tk_var(self):
        for a, b in zip(self.dict_btn.values(), self.dict_tk_var.values()):
            print('Var: ', b.get(), ' Btn State: ', a['state'])
