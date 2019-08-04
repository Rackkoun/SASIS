"""
    Created on 23.07.2019 at 16:40
    @author: Ruphus
"""
from tkinter.ttk import Radiobutton


class SASISRadioButton:

    def __init__(self, root, lname, rad_val, tk_int_var=None):
        """
        Beim Erstellen eines RadioButtons wird sich hier auf die Option 'indicatoron' verzichtet,
        welche die gewoehnliche Form eines RadioButton-Elementen zu dieser eines (normalen)
        Buttons darstellen laesst.

        :param root: Frame, in dem das RadioButton-Element gepackt wird
        :param lname: Name des RadioButton
        :param tk_int_var: ein Int-Variable (Object) der Tk-Klasse.
        :param rad_val: Werte des RadioButtons, wird fuer die Aktierung durch die tk_int_var verglichen
        """
        # self.master_lf = None # wird spaeter implementiert
        self.rdio = Radiobutton(master=root, text=lname, variable=tk_int_var,
                                value=rad_val, command=None)

    def get_rbtn(self):
        return self.rdio
    # def set_btn_pos(self, col, row, px, py):
    #     self.rdio.grid(row=row, column=col, padx=px, pady=py, sticky='W')
    #     pass

    # def set_master_lf(self, mlf):
    #   """

    #   :param mlf: Bezug entweder auf die obere oder die untere Darstellung
    #   :return:
    #    """
    #    self.master_lf = mlf
