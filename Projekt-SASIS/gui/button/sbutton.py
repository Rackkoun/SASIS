"""
Created on 20.07.2019
https://docs.python.org/3/library/tkinter.html
https://tkdocs.com/tutorial/styles.html
@author: Ruphus

source: Threading: https://automatetheboringstuff.com/chapter15/
                   https://www.devdungeon.com/content/gui-programming-python#threads
"""
from tkinter import Button
from tkinter import RAISED

class SASISActionButton:
    """
    """

    def __init__(self, root):
        """

        :param root:
        :param master_lf:
        """
        #self.master_lf = master_lf
        self.btn = Button(master=root, text='OFF', state='normal', command=None, bg='#00bfff', fg='#ffffff', relief=RAISED)
        pass

    def get_btn(self):
        return self.btn

