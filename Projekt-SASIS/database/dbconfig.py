"""
    Created on 03.08.2019 at 14:18
    @author: Ruphus
    sources: https://www.andreafiori.net/posts/connecting-to-a-postgresql-database-with-python
             https://www.dev2qa.com/how-to-connect-postgresql-server-use-configuration-file-in-python/
"""
import os.path
from configparser import ConfigParser


class DBConfiguration:
    """
        Skript-Datei für die Initialisierung der Verbindung zu der Datenbank
        @:var: file_path: Pfad bis zu dem Konfig-Datei
    """
    file_path = '../res/config/'  # zwei Punkt erforderlich für die Sichtbarkeit des Ordners

    def __init__(self):
        """
         @:var: parsedatei: ConfigParser-Objekt, welches die Informationen in der dbconfig.ini-Datei liest und
                damit eine Verbindung zu der DB-Server erstellt.
        """
        self.parsefile = ConfigParser()
        self.parsefile.read(os.path.join(DBConfiguration.file_path, 'dbconfig.ini'))
        pass

    def on_parsing_file(self):
        """
            Die Methode wird die Informationen in der ini-Datei zu einem Python-Wörterbuch umwandeln
            Die Hinweis zwische eckigen Klammern in der Datei dienen zur Erstellung von
            Wörterbuch-Elementen.
            Am Ende des Prozess wird eine konsistente Wörterbuch-Variable für die Verbindung zu der Datenbank
            zurückgegeben
        :return: dict_db
        """
        dict_db = {}
        if self.parsefile.has_section('Verbrauch'):
            parameters = self.parsefile.items('Verbrauch')
            for param in parameters:
                dict_db[param[0]] = param[1]
        else:
            raise Exception('Sektion nicht gefunden in File {0}'.format(self.parsefile))

        return dict_db
