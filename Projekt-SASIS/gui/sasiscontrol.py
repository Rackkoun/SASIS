import tkinter as tk
from tkinter.ttk import Notebook

from gui.frame.electricitypanel import ApplianceDeviceControl as elecpanel
from gui.frame.graphpanel import MonitorringControl as monitorpanel
from gui.frame.databasepanel import DatabaseContent as dbpanel
""" Diese Klasse stellt das Interface fuer die Kontrolle des gesamten Anwendungssystems dar.
"""


class SASISCommandInterface:

    def __init__(self):
        """
        Initialisierung aller Komponenenten des Systems
        """
        self.wmain = tk.Tk()  # Hauptfenster
        self.wtab = Notebook()  # Reiter-Erstellung in dem Hauptfenster
        self.elect_panel_tab = elecpanel(self.wtab)  # Erste Reiteransicht: Strom und Bildplan
        self.graph_tab = monitorpanel(self.wtab)  # Zweite Reiteransicht: Graphen und Algorithmen fuer die Darstellung
        self.db_tab = dbpanel(self.wtab)

        self.on_create_window()  # Initialisierung aller Elementen in Reitern

        pass

    def on_create_window(self):
        """
        Methode fuer die Initialisierung von Elementen sowohl in dem Hauptfenster als auch in allem Reiter
        :return:
        """
        self.wmain.title('SASIS Control Interface')
        self.wmain.resizable(False, False)

        print("Width: ", self.wmain.winfo_screenwidth(), "height: ", self.wmain.winfo_screenheight())
        self.wtab.add(self.elect_panel_tab.get_panel(), text="Steuerungsansicht")
        self.elect_panel_tab.on_create_labelframe('Steuerungspanel', 0, 0, 8, 10, 'N')
        self.elect_panel_tab.on_create_labelframe('Wohnungsarchitektur', 2, 0, 8, 10, 'N', 'NICHST')

        self.elect_panel_tab.create_new_intern_label('Bezeichner:', 0, 0, 8, 8, 'W')
        self.elect_panel_tab.create_new_intern_label('Zustand:', 1, 0, 8, 8, 'W')

        self.elect_panel_tab.on_adding_basic_appliance('WZ', 0, 1, 8, 8, 'W')
        self.elect_panel_tab.on_adding_basic_appliance('SZ', 0, 2, 8, 8, 'W')
        self.elect_panel_tab.on_adding_basic_appliance('WC', 0, 3, 8, 8, 'W')
        self.elect_panel_tab.on_adding_basic_appliance('DUSCHE', 0, 4, 8, 8, 'W')
        self.elect_panel_tab.on_adding_basic_appliance('WZ + K', 0, 5, 8, 8, 'W')
        self.elect_panel_tab.on_adding_basic_appliance('WZ + K + KP4', 0, 6, 8, 8, 'W')
        self.elect_panel_tab.on_adding_basic_appliance('WZ + K + WM4', 0, 7, 8, 8, 'W')
        self.elect_panel_tab.on_adding_basic_appliance('WZ + K + KP4 + WM4', 0, 8, 8, 8, 'W')
        self.elect_panel_tab.on_adding_basic_appliance('ALLES EIN', 0, 9, 8, 8, 'W')
        self.elect_panel_tab.on_adding_basic_appliance('ALLES AUS', 0, 10, 8, 8, 'W')

        self.wtab.add(self.graph_tab.master, text='Graphenansicht')

        self.graph_tab.on_create_labelframe('Aktualisierung der oberen Graphen', 0, 0, 8, 10, 'NW')
        self.graph_tab.add_btn(0, 0, 8, 8)

        self.graph_tab.on_create_labelframe('Maschinelles Lernen Algorithmen', 0, 1, 8, 10, 'NW')
        self.graph_tab.add_rbtn('Isolation Forest', 1, 0, 0, 8, 8)
        self.graph_tab.add_rbtn('Elliptic Envelope', 2, 0, 1, 8, 8)
        self.graph_tab.add_rbtn('Local Outliers Factor', 3, 0, 2, 8, 8)
        self.graph_tab.add_rbtn('One Class SVM', 4, 0, 3, 8, 8)

        self.graph_tab.on_create_frame_up_lf(frame_name='Darstellumg mit groben Daten', col=1, row=0, colpad=5,
                                             rowpad=5)
        self.graph_tab.on_add_graph_up(grp_style='line', col=0, row=0, px=3, py=3)
        self.graph_tab.on_add_graph_up(grp_style='scatter', col=1, row=0, px=3, py=3)
        self.graph_tab.on_add_graph_up(grp_style='box', col=2, row=0, px=3, py=3)
        self.graph_tab.on_add_graph_up(grp_style='bar', col=3, row=0, px=3, py=3)

        self.graph_tab.on_create_frame_down_lf(frame_name='Darstellung mit trainierten Daten', col=1, row=1, colpad=5,
                                               rowpad=5)
        self.graph_tab.on_add_graph_down(algo_name='Isolation Forest', col=1, row=0, px=3, py=3, x=[], y=[],
                                         x1=[], y1=[], x2=[], y2=[])
        self.graph_tab.on_add_graph_down(algo_name='Elliptic Envelope', col=2, row=0, px=3, py=3, x=[], y=[],
                                         x1=[], y1=[], x2=[], y2=[])
        self.graph_tab.on_add_graph_down(algo_name='Local Outliers Factor', col=3, row=0, px=3, py=3, x=[], y=[],
                                         x1=[], y1=[], x2=[], y2=[])
        self.graph_tab.on_add_graph_down(algo_name='One Class SVM', col=4, row=0, px=3, py=3, x=[], y=[],
                                         x1=[], y1=[], x2=[], y2=[])

        self.wtab.add(self.db_tab.master, text='Datenbankansicht')

        self.db_tab.on_create_labelframe('Datebank Aktion-Button', col=0, row=0, px=8, py=8, pos='NW')
        self.db_tab.add_btn(col=0, row=0, colpad=8, rowpad=8)

        self.db_tab.on_create_labelframe('Datenbankinhalt', col=1, row=0, px=5, py=8, pos='E')
        self.db_tab.on_create_label('ID', col=1, row=0, colpad=3, rowpad=5, pos='N')
        self.db_tab.on_create_label('STROMVERBRAUCH', col=2, row=0, colpad=3, rowpad=5, pos='N')
        self.db_tab.on_create_label('DATUM', col=3, row=0, colpad=3, rowpad=5, pos='N')

        self.db_tab.on_create_field(col=1, row=1, px=8, py=8, cspan=3)

        self.db_tab.on_create_labelframe('Datenbankstatistiken: ', col=2, row=0, px=8, py=8, pos='N')
        self.db_tab.on_create_label('min Verbrauch: ', col=2, row=0, colpad=8, rowpad=8, pos='N')
        self.db_tab.on_create_label('max Verbrauch: ', col=2, row=1, colpad=8, rowpad=8, pos='N')
        self.db_tab.on_create_label('akt Verbrauch: ', col=2, row=2, colpad=8, rowpad=8, pos='N')
        self.wtab.pack(expand=1, fill='both')
        pass

    def start_app(self):
        """
        Endlos-Starten des Programms
        :return:
        """

        self.wmain.mainloop()
