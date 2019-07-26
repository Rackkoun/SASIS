"""
Created on 20.07.2019
https://docs.python.org/3/library/tkinter.html
https://tkdocs.com/tutorial/styles.html
@author: Ruphus
"""
import os.path
from tkinter.ttk import Button, Label
from PIL import Image, ImageTk
from model.constants.pictures import HousePlan
from model.elementdict.labelmodel import LabelModel

class SASISActionButton:
    """Ereigniskalsse fuer Buttons (Radio, normale Buttons usw.)

    Ein Label Model wird wegen des Objeckt-Unterschieds:
    folgender Fehler geschiedt, wenn das Modell in einer anderen Klasse erzeugt wird
    und dann später einen Befehl (command) uebergeben wird
    Fehler: KeyError: "<tkinter.ttk.Button object .!notebook.!frame.!labelframe.!button8>"
    Button position wird troztdem erkannt, aber nicht als dasselbe Objekt
    """

    def __init__(self, root, name_btn, room_name, master_lf=None):
        """

        :param root:
        :param name_btn:
        :param room_name:
        :param master_lf:
        """
        self.master_lf = master_lf
        self.btn = Button(master=root, text=name_btn, command=self.reload_plan)
        #self.btn.configure(command=lambda :self.reload_plan)
        self.mbtn = LabelModel(room_name)
        self.mbtn.obj = self.btn

        self.filepath = os.path.dirname('./res/img/')
        self.plan = HousePlan().load_plan
        pass

    def set_btn_pos(self, col, row, px, py):
        self.btn.grid(row=row, column=col, padx=px, pady=py)
        pass

    def reload_plan(self):
        """ Diese Methode aktualisiert den Plan wenn ein Button geklickt wird
            source book python and tkinter programming (2000): code about sensors and LED
        """
        if self.mbtn.name == 'WZ':
            if self.btn['text'] == 'OFF':
                self.btn['text'] = 'ON'
                self.on_updated_action(self.mbtn.name)
            else:
                self.on_reset_action()

        elif self.mbtn.name == 'SZ':
            if self.btn['text'] == 'OFF':
                self.btn['text'] = 'ON'
                self.on_updated_action(self.mbtn.name)
            else:
                self.on_reset_action()

        elif self.mbtn.name == 'WC':
            if self.btn['text'] == 'OFF':
                self.btn['text'] = 'ON'
                self.on_updated_action(self.mbtn.name)
            else:
                self.on_reset_action()

        elif self.mbtn.name == 'DUSCHE':
            if self.btn['text'] == 'OFF':
                self.btn['text'] = 'ON'
                self.on_updated_action(self.mbtn.name)
            else:
                self.on_reset_action()

        elif self.mbtn.name == 'WZ + K':
            if self.btn['text'] == 'OFF':
                self.btn['text'] = 'ON'
                self.on_updated_action(self.mbtn.name)
            else:
                self.on_reset_action()

        elif self.mbtn.name == 'WZ + K + KP4':
            if self.btn['text'] == 'OFF':
                self.btn['text'] = 'ON'
                self.on_updated_action(self.mbtn.name)
            else:
                self.on_reset_action()

        elif self.mbtn.name == 'WZ + K + WM4':
            if self.btn['text'] == 'OFF':
                self.btn['text'] = 'ON'
                self.on_updated_action(self.mbtn.name)
            else:
                self.on_reset_action()

        elif self.mbtn.name == 'WZ + K + KP4 + WM4':
            if self.btn['text'] == 'OFF':
                self.btn['text'] = 'ON'
                self.on_updated_action(self.mbtn.name)
            else:
                self.on_reset_action()

        elif self.mbtn.name == 'ALLES EIN':
            if self.btn['text'] == 'OFF':
                self.btn['text'] = 'ON'
                self.on_updated_action(self.mbtn.name)
            else:
                self.on_reset_action()

        elif self.mbtn.name == 'ALLES AUS':
            if self.btn['text'] == 'OFF':
                self.btn['text'] = 'ON'
                self.on_updated_action(self.mbtn.name)
            else:
                self.on_reset_action()

        else:
            pass
            #self.reset_action()



        # return self.on_btn_clicked(b_grp, p_grp, btn, img_path, lbl)

    def get_btn(self):
        return self.btn
    # method could be loaded on a thread, so we have to check if the thread-instance
    # is always alive
    def on_updated_action(self, btn_obj_name):
        """

        :param btn_obj_name:
        :return:
        """
        try:
            # img = Image.open(str(self.plan[rname]))
            img = Image.open(os.path.join(self.filepath, self.plan[btn_obj_name]))

            img.rotate(90)
            img.thumbnail((884, 400), Image.ANTIALIAS)
            tmp_lbl = ImageTk.PhotoImage(image=img)
            Label(self.master_lf, image=tmp_lbl).grid(column=0, row=0, padx=8, pady=5)
            self.master_lbl = tmp_lbl
            print(btn_obj_name, ' STATUS: ', self.btn['text'])
        except IOError as ierror:
            print('Fehler beim Laden des Bildes: -->', ierror)
        except KeyError as kerror:
            print('Variable nicht erkannt: --> ', kerror)

    def on_reset_action(self):
        """

        :return:
        """
        if self.btn['text'] == 'ON':
            self.btn['text'] = 'OFF'
            try:
                # img = Image.open(str(self.plan[rname]))
                img = Image.open(os.path.join(self.filepath, self.plan['NICHST']))
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                tmp_lbl = ImageTk.PhotoImage(image=img)
                Label(self.master_lf, image=tmp_lbl).grid(column=0, row=0, padx=8, pady=5)
                self.master_lbl = tmp_lbl
                print('Reset to: ', 'NICHST', ' STATUS: ', self.btn['text'])
            except IOError as ierror:
                print('Fehler beim Laden des Bildes: -->', ierror)
            except KeyError as kerror:
                print('Variable nicht erkannt: --> ', kerror)

    # does not have an effect, will be ignore in this implementation
    def on_updated(self, name):
        for k in self.plan.keys():
            if k == name and self.btn['text'] == 'ON':
                self.on_updated_action(name)
            if not name and self.btn['text'] == 'ON':
                self.btn['text'] = 'OFF'
            #else:
            #    self.on_reset_action()