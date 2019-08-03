"""
Created on 21.07.2019 at 14:42
@author: Ruphus
Diese Klasse erhaelt nur Konstantenwerte, welcher Namen seinen entsprechenden Plan auf dem Bild zugeordnet sind.
"""


class HousePlan:

    def __init__(self):
        """
        Beim Erstellen eines Housplan-Objekt, wird das Woerterbuch geladen
        """
        self.load_plan = {}
        self.on_load()

    def on_load(self):
        """
        Woerterbuch, welches einen Bezeichner fuer einen Raum mit dementsprechden Plan (Bild) mappt
        :return:
        """
        self.load_plan = {
            'WZ': 'wohnung-architektur-wohnzimmer-ein.png',
            'SZ': 'wohnung-architektur-schlafzimmer-ein.png',
            'WC': 'wohnung-architektur-wc-ein.png',
            'DUSCHE': 'wohnung-architektur-dusche-ein.png',
            'WZ + K': 'wohnung-architektur-wohnzim-und-kueche-ein.png',
            'WZ + K + KP4': 'wohnung-architektur-wohnzim-und-kueche-kp4-ein.png',
            'WZ + K + WM4': 'wohnung-architektur-wohnzim-und-kueche-wm4-ein.png',
            'WZ + K + KP4 + WM4': 'wohnung-architektur-wohnzim-und-kueche-wm4-kp4-ein.png',
            'ALLE LICHTER EIN': 'wohnung-architektur-alle-lichter-ein.png',
            'ALLE LICHTER AUS': 'wohnung-architektur-alles-aus.png',
            'NICHST': 'wohnung-architektur.png'
        }

    def get_plan(self):
        return self.load_plan
