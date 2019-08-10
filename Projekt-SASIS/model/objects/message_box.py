"""
    Created on 07.08.2019 at 16:05
    @author: Ruphus
    source: Python gui programming cookbook (book)
            https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
"""

from tkinter import Toplevel, Label, LEFT, SOLID
class MessageTip:

    def __init__(self, gui, msg):
        self.gui = gui
        self.tip = None
        self.id = None
        self._ide = self.gui.bind('<Enter>', self.on_entry)
        self._idl = self.gui.bind('<Leave>', self.on_leave)
        self.msg = msg
        self.x = self.y = 0

    def show(self):
        "Display text in tooltip window"
        if self.tip or not self.msg:
            return
        x, y, _cx, cy = self.gui.bbox("insert")
        x = x + self.gui.winfo_rootx() + 27
        y = y + cy + self.gui.winfo_rooty() + 27
        self.tip = tw = Toplevel(self.gui)

        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        Label(master=self.tip,  text=self.msg, justify=LEFT, background='#ffffe0', relief=SOLID, borderwidth=1).pack()

    def hidetip(self):
        tw = self.tip
        self.tip = None
        if tw:
            tw.destroy()

    def on_entry(self, event=None):
        self.check()
        self.show()

    def on_leave(self, event=None):
        self.check()
        self.hidetip()

    def check(self):
        id = self.id
        self.id = None
        if id:
            self.gui.after_cancel(id)