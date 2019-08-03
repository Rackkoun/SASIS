"""
    Created on 03.08.2019 at 14:32
    @author: Ruphus

    sources: http://initd.org/psycopg/docs/usage.html
             https://pynative.com/python-postgresql-tutorial/
"""
import psycopg2
import datetime as dt
import pandas as pd
from database.dbconfig import DBConfiguration


class PostgreSQLDatabase:
    """
        Klasse für die Verwaltung von Daten in dem Postgres-Server (Daten Schreiben und Lesen).
    """

    def __init__(self):
        """
        @var: connection: Variable für die Abfrage der Verbindung zu der Server
              Die Verbindung wird nicht direkt erstellt, wenn eine Instanz dieser Klasse erzeugt ist
        @var: db_config:
        """
        self.connection = None
        self.db_config = DBConfiguration()
        print("Konfig-Datein erfolgreich geladen")
        pass

    def in_connecting(self):
        """
            Bearbeite die Informationen in der Konfig-Datei und erstelle damit
            eine Verbindung
            :return: Kein:
        """
        try:
            login_info = self.db_config.on_parsing_file()
            print('Verbindung zur der Datenbank wird hergestellt ...')
            self.connection = psycopg2.connect(**login_info)
            print('Verbindung ist hersgestellt!')
        except (Exception, psycopg2.DatabaseError) as dbfehler:
            print('Verbindung ist nicht hergestellt worden \n', dbfehler)
        return self.connection


    def write_new_values(self, strom):
        """
            nehme ein neuer Stromverbrauch als Parameter und schreibe ihn in der Datenbank
            :param strom: Neuer Stromverbrauch
            :return: Kein
        """
        query = ''' INSERT INTO verbrauch (strom, datum) \
                    VALUES (%s, %s)
                '''
        date_var = dt.date.today() # das aktuelle Datum immer eintragen
        values = (strom, date_var) # speichere die Werte als Tuple

        try:
            curs = self.connection.cursor()         # erzeuge ein Cursor-Objekt
            curs.execute(query, values)             # schreibe values in den gegebenen Spalten in query
            self.connection.commit()                # dann schicke die Anfrage zu dem Server
            nbr_of_row = curs.rowcount
            print("Number of Rows: ", nbr_of_row)
        except (Exception, psycopg2.Error) as dberror:
            if self.connection:
                print("Fehler beim Einfügen der Daten in der DB: ",dberror)
                self.connection.rollback()         # db zurücksetzen
        finally:
            if self.connection:
                curs.close()                       # schließe der Cursor aber nicht die Verbindung (Zum Testen)
                print("Cursor geschlossen")


    def read_db_content(self):
        """
            Lese der komplette Inhalt der Datenbank und Erstelle eine Tabelle damit
            :return: df: Pandas-DataFrame-Objekt, welche der Inhalt der DB erhält (wird noch Vorverarbeitet)
        """
        df = None
        try:
            curs = self.connection.cursor()  # erstelle eine Verbindung zu dem Server
            query = '''
                                SELECT * FROM verbrauch
                            '''
            curs.execute(query)  # mit dem Befehl query
            db_content = curs.fetchall()  # dann lese den kompletten Inhalt
            print("DB-Inhalt vor der Bearbeitung mit Pandas:\n")
            for content in db_content:
                print('verbrauch_id: ', content[0])
                print('strom: ', content[1])
                print('datum: ', content[2])
            print("\nDB-Inhalt nach der Bearbeitung mit Pandas:\n")
            cols = ['id', 'strom', 'datum']  # die Abfrage erfordert die Index-Spalte zu erstellen, sonst führt zur Fehler
            df = pd.DataFrame(db_content, columns=cols, index=None)
            print("Vor der Bearbeitung ")
            print(df)
            #df = self.on_preprocessing_data(data=df)

        except (Exception, psycopg2.Error) as dberror:
            print("Fehler beim Lesen des DB-Inhalts", dberror)
            self.connection.rollback()
        finally:
            if self.connection:
                curs.close()
                print("Cursor geschlossen")
        return df

    def on_preprocessing_data(self, data):
        """
        source: https://stackoverflow.com/questions/18022845/pandas-index-column-title-or-name
            Vorbereitung der Daten für eine Bearbeitung mit den Maschellen Lernen-Algorithmen
            :param data: Pandas-DataFrame-Objekt
            :return: data
        """
        values = data['strom'].values # speiche die Werte vor der Umwandlung ansonsten geht sie verloren
        reconverted_date = pd.to_datetime(data['datum']) # wandere das Datum um

        frame = pd.DataFrame(columns=['strom'], index=reconverted_date) # erstelle ein neues Frame mit Datum als Index
        frame['strom'] = values # gebe die gespeicherten Werte in dem neuen Frame zurück
        frame['tag'] = frame.index.day
        frame['monat'] = frame.index.month
        frame['jahr'] = frame.index.year
        frame['wochentag'] = frame.index.weekday_name
        print("nach der Bearbeitung")
        print(frame, '\n', frame.dtypes)
        #print(data)
        return frame
if __name__=="__main__":
    db =PostgreSQLDatabase()
    db.in_connecting()

    #db.write_new_values(545.96)
    data = db.read_db_content()
    db.on_preprocessing_data(data=data)
    data.head(2)