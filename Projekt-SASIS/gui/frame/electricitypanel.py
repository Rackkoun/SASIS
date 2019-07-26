import os.path
from tkinter.ttk import Frame, LabelFrame, Label
from PIL import Image, ImageTk
from gui.button.sbutton import SASISActionButton as sButton
from exceptions.labelexception import LabelAlreadyExistException
from model.elementdict.labelmodel import LabelModel
from model.constants.pictures import HousePlan

"""@author: Ruphus
   Created on 20.07.2019 """


class ApplianceDeviceControl:
    """ Diese Klasse ist fuer die Darstellung von Steuerelemente fuer den Strom verantwortlich
    z. B.: Lichte, Waschmaschine, Fernseher. usw."""

    def __init__(self, root):
        """

        :param root:
        """
        self.dev_control_panel = Frame(master=root)
        self.panel_control_lf = None
        self.intern_lbls = {}
        self.btn_grp = {}
        self.house_plan_lf = None
        self.house_lbl = None
        # self.activ_btn = sButton()
        self.filepath = './res/img/'
        self.plan = HousePlan().load_plan
        pass

    def get_panel(self):
        # self.dev_control_panel.grid(column=col, row=row, padx=colpad, pady=rowpad, sticky=position)
        return self.dev_control_panel

    def add_basic_appliance(self, roon_name, col, row):
        mlabel = LabelModel(roon_name)
        mbtn = LabelModel(roon_name)

        mlabel.obj = Label(master=self.panel_control_lf, \
                           text=mlabel.name)
        mlabel.obj.grid(column=col, row=row, padx=8, pady=8, sticky='W')
        ##   -------- hsuhsuhghisd ----- Enleer le status
        mbtn.obj = self.add_btn(mbtn.name,'OFF', col=col + 1, row=row, colpad=8,
                                rowpad=8)  # .winfo_id() # id des Buttons speichern

        ##### #### # ## #
        self.intern_lbls[mlabel.name] = mlabel.obj
        self.btn_grp[mbtn.name] = mbtn.obj

        self.update_plan()

    def create_new_intern_label(self, label_name, col, row, colpad, rowpad, pos):
        if label_name in self.intern_lbls:
            pass
            # raise LabelAlreadyExistException(label_name, 'Already exists!')
        else:
            mlab = LabelModel(label_name)
            mlab.obj = Label(master=self.panel_control_lf, \
                             text=mlab.name)
            mlab.obj.grid(column=col, row=row, \
                          padx=colpad, pady=rowpad, sticky=pos)

            self.intern_lbls[mlab] = mlab.obj

        return self.intern_lbls

    def on_create_labelframe(self, frame_name, col, row, colpad, rowpad, pos, pic=None):

        if pic == None:

            self.panel_control_lf = LabelFrame(master=self.dev_control_panel, \
                                               text=frame_name)
            self.panel_control_lf.grid(column=col, row=row, padx=colpad, \
                                       pady=rowpad, sticky=pos)
            # return self.panel_control_lf
        else:
            self.house_plan_lf = LabelFrame(master=self.dev_control_panel, \
                                            text=frame_name)
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
            img_lbl = ImageTk.PhotoImage(
                image=img)  # ohne dass --> UnboundLocalError: local variable 'img' referenced before assignment
            self.house_lbl = Label(self.house_plan_lf,
                                   image=img_lbl)  ## ohne dass - - > _tkinter.TclError: image specification must contain an odd number of elements
            self.house_lbl.grid(column=0, row=0, padx=8, pady=5)
            self.house_lbl = img_lbl  # und diese Zuweisung am Ende

    def add_btn(self, room, status, col, row, colpad, rowpad):  # enlever le status
        btn = sButton(root=self.panel_control_lf,room_name=room, name_btn=status,\
                      master_lf=self.house_plan_lf)

        btn.set_btn_pos(col, row, colpad, rowpad)

        return btn.get_btn()

    def update_plan(self):
        for (p, n) in zip(self.plan.keys(), self.plan.values()):
            print(p, ' >>> ', n)
        print('\n\n-------  Button  ----------------:\n')
        for (key, val) in zip(self.btn_grp.keys(), self.btn_grp.values()):
            #    if val:
            print(key, '- - - ', val, ': Button')

    def reload_plan(self, btn):
        """ Diese Methode aktualisiert den Plan wenn ein Button geklickt wird """
        for k, v in zip(self.btn_grp.keys(), self.btn_grp.values()):
            if btn.btn.winfo_id() == v.winfo_id():
                try:
                    img = Image.open(os.path.join( \
                        os.path.dirname(self.filepath), \
                        self.plan[v]))
                except IOError as error:
                    print('Bild kann nicht geladen werden, Grund: ', error)
                img.rotate(90)
                img.thumbnail((884, 400), Image.ANTIALIAS)
                self.house_lbl = ImageTk.PhotoImage(image=img)
                btn.btn['text'] = 'ON'
            else:
                btn.btn['text'] = 'OFF'