"""
    Created on 23.07.2019 at 16:40
    @author: Ruphus
"""
from tkinter.ttk import Radiobutton, Label
class SASISRadioButton:

    def __init__(self, root, name, rad_val, tk_int_var=None):
        """
        Beim Erstellen eines RadioButtons wird sich hier auf die Option 'indicatoron' verzichtet,
        welche die gewoehnliche Form eines RadioButton-Elementen zu dieser eines (normalen)
        Buttons darstellen laesst.

        :param root: Frame, in dem das RadioButton-Element gepackt wird
        :param name: Name des RadioButton
        :param tk_int_var: ein Int-Variable (Object) der Tk-Klasse.
        :param rad_val: Werte des RadioButtons, wird fuer die Aktierung durch die tk_int_var verglichen
        :param master_lf: Das Element wird einer LabelFrame zugeordnet
        """
        self.master_lf = None # wird spaeter implementiert
        self.rdio = Radiobutton(master=root, text=name, variable=tk_int_var,\
                                value=rad_val)

    def set_btn_pos(self, col, row, px, py):
        self.rdio.grid(row=row, column=col, padx=px, pady=py)
        pass

    def set_master_lf(self, mlf):
        """

        :param mlf: Bezug entweder auf die obere oder die untere Darstellung
        :return:
        """
        self.master_lf = mlf