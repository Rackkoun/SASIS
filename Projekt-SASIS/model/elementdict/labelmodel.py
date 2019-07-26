""" python 3 oop
    Created on 20.07.2019, 21:50
    @:author: Ruphus

    @:param: lname: Bezeichner (name)
    @:param: obj: Element (Label, Button, usw.)
"""

class LabelModel:
    """ Die Label und LabelFrame-Darstellungen in dem Programm besitzen dieselbe
        Struktur. Somit wird ein Woerterbuch erstellt, welches der Bezeichner fuer einen Raum ueberprueft.

        Das Model wird auch fuer anderen GUI-Elemente wie z. B.:
        Button verwendet
    """

    def __init__(self, lname, obj=None):
        """

        :param lname: Bezeichner
        :param obj: Es kann sich hier um ein Label, LabelFrame, Button oder ein anderes Objekt handeln
        """
        self.name = lname
        self.obj = obj

    def check_name(self, name):
        """pruefe nach dem gegebenen Namen """
        return self.name == name
