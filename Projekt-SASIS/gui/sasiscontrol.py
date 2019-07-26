import tkinter as tk
from tkinter.ttk import Notebook

from gui.frame.electricitypanel import ApplianceDeviceControl as elecpanel
from gui.frame.graphpanel import MonitorringControl as monitorpanel

""" Diese Klasse stellt das Interface fuer die Kontrolle des gesamten Anwendungssystems dar.
"""

class SASISCommandInterface:



    def __init__(self):
        """
        Initialisierung aller Komponenenten des Systems
        """
        self.wmain = tk.Tk()                             # Hauptfenster
        self.wtab = Notebook()                           # Reiter-Erstellung in dem Hauptfenster
        self.elect_panel_tab = elecpanel(self.wtab)      # Erste Reiteransicht: Strom und Bildplan
        self.graph_tab = monitorpanel(self.wtab)         # Zweite Reiteransicht: Graphen und Algorithmen fuer die Darstellung
        self.var_up = tk.IntVar()                        # Tk-Integer-Variable: wird fuer die RadionButton gebraucht, um zu wissen, welcher Button ausgewaehlt ist
        self.var_down = tk.IntVar()
        self.on_create_window()                          # Initialisierung aller Elementen in Reitern


        pass

    def on_create_window(self):
        """
        Methode fuer die Initialisierung von Elementen sowohl in dem Hauptfenster als auch in allem Reiter
        :return:
        """
        self.wmain.title('SASIS Control Interface')
        print("Width: ", self.wmain.winfo_screenwidth(), "height: ", self.wmain.winfo_screenheight())
        self.wtab.add(self.elect_panel_tab.get_panel(), text="Steuerungsansicht")
        self.elect_panel_tab.on_create_labelframe('Steuerungspanel', \
                                                  0, 0, 8, 10, 'N')
        self.elect_panel_tab.on_create_labelframe('Wohnungsarchitektur', 2, 0, 8, 10, 'N', 'NICHST')

        self.elect_panel_tab.create_new_intern_label('Bezeichner:', \
                                                     0, 0, 8, 8, 'W')
        self.elect_panel_tab.create_new_intern_label('Zustand:', \
                                                     1, 0, 8, 8, 'W')
        self.elect_panel_tab.add_basic_appliance('WZ', 0, 1)
        self.elect_panel_tab.add_basic_appliance('SZ', 0, 2)
        self.elect_panel_tab.add_basic_appliance('WC', 0, 3)
        self.elect_panel_tab.add_basic_appliance('DUSCHE', 0, 4)
        self.elect_panel_tab.add_basic_appliance('WZ + K', 0, 5)
        self.elect_panel_tab.add_basic_appliance('WZ + K + KP4', 0, 6)
        self.elect_panel_tab.add_basic_appliance('WZ + K + WM4', 0, 7)
        self.elect_panel_tab.add_basic_appliance('WZ + K + KP4 + WM4', 0, 8)
        self.elect_panel_tab.add_basic_appliance('ALLES EIN', 0, 9)
        self.elect_panel_tab.add_basic_appliance('ALLES AUS', 0, 10)

        self.wtab.add(self.graph_tab.master, text='Graphenansicht')
        self.graph_tab.on_create_labelframe('Option UP Radio', 0, 0, 8, 10, 'NW')
        self.graph_tab.add_rbtn('radio up', 1, 0, 0, 8, 8, tk_var=self.var_up)
        self.graph_tab.on_create_labelframe('Option Down Radio', 0, 1, 8, 10, 'SW')
        self.graph_tab.add_rbtn('radio down', 1, 0, 0, 8, 8, tk_var=self.var_down)
        self.graph_tab.on_create_glabelframe('Graph Up', 1, 0, 8, 10, 'NE')
        #self.graph_tab.on_draw_graph(xdata=[2,8,3,-5,7,5,16], ydata=[0,4,8,2,1,8,9],\
        #                            xlabel='X Label 1', ylabel='Y Label 1',\
        #                            color='r', style='dashed')
        self.graph_tab.onDraw(x=[2, 8, 3, -5, 7, 5, 16], y=[0, 4, 8, 2, 1, 8, 9], \
                                     lx='X Label 2', ly='Y Label 2', \
                                     c='b', s='dashed')
        self.graph_tab.onDraw(x=[2, 8, 3, -5, 7, 5, 16], y=[0, 4, 8, 2, 1, 8, 9], \
                              lx='X Label 2', ly='Y Label 2', \
                              c='g', s='dashed')
        self.graph_tab.onDraw(x=[2, 8, 3, -5, 7, 5, 16], y=[0, 4, 8, 2, 1, 8, 9], \
                              lx='X Label 2', ly='Y Label 2', \
                              c='r', s='dashed')
        #self.graph_tab.on_draw_graph2(xdata=[2, 8, 3, -5, 7, 5, 16], ydata=[0, 4, 8, 2, 1, 8, 9], \
        #                             xlabel='X Label 3', ylabel='Y Label 3', \
        #                             color='g', style='dashed')
        #self.graph_tab.add_grah_to_frame(col=1, row=0, xpad=8, ypad=8)
        self.graph_tab.on_create_labelframe('Graph Down', 1, 1, 8, 10, 'SE')
        self.graph_tab.add_rbtn('graph south east', 1, 0, 0, 8, 8, tk_var=self.var_down)
        self.wtab.pack(expand=1, fill='both')
        pass

    #def add_intern_label(self, master):

    def lauchApp(self):
        """
        Endlos-Starten des Programms
        :return:
        """
        self.wmain.mainloop()