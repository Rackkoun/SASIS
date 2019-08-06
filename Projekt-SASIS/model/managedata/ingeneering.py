"""
    Created on 2019-08-05 at 14:58
    @author: Ruphus
    Bearbeite die Daten für das Lernen mit dem Maschinellen Lernen

    sources: datetime: https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python
             append df: https://www.geeksforgeeks.org/python-pandas-dataframe-append/
             https://stackoverflow.com/questions/46343773/add-to-a-dataframe-as-i-go-with-datetime-index
"""
import datetime as dt
import pandas as pd


class DataProcessing:

    def __init__(self):
        pass

    def on_getting_data_from_server(self, data):
        grp = data.groupby('datum')['strom'].sum()  # erzeuge ein Serie-Objekt
        reconverted_index = pd.to_datetime(grp.index)  # wandle das Index-Format in datetime um
        df = pd.DataFrame(grp.values, columns=['strom'], index=reconverted_index)  # erstelle ein Dataframe-Objekt
        df.index.name = None  # lösche den Index-Name in dem Datafram-Objekt, dann füge weitere Spalten hinzu

        df['tag'] = df.index.day
        df['monat'] = df.index.month
        df['jahr'] = df.index.year
        df['wochentag'] = df.index.weekday_name

        return df  # gibt das Dataframe zurück

    def split_for_sasis(self, df):
        X1 = df.iloc[:, [0, 1]].values
        return X1

    def after_train_or_predict_data(self, df, predict_set):
        df['vorhersage'] = predict_set
        return df

    def on_actualize_data_dict(self, current_df, old_df):
        old_df = old_df.append(current_df)
        old_df = old_df.sort_index(axis=0)

        return old_df

    def detect_outliers(self, df):
        out0 = df[df['vorhersage'] == -1]
        out = out0[out0['strom'] > 4019.59]
        return out

    def select_current_value(self, df):
        print("Before, len: ", len(df))
        current = df[df.index.date == dt.date.today()]
        print("After, len: ", len(current))
        return current

#
# if __name__=='__main__':
#     test = TestDataGenerator()
#     ing = DataProcessing()
#     algo = OneCSVM()
#
#     db = server()
#     #f = './res/config/dbconfig.ini'
#     #conn = db.in_connecting(file_name=f)
#     data = test.on_create_test_data('2019-04-01', '2019-07-01', 'D', .3)
#     X = ing.split_for_sasis(data)
#     algo.train_one_csvm(X)
#     pred0 = algo.predict_one_csvm(X)
#     data2 = ing.after_train_or_predict_data(data, pred0)
#     x = [[4217.45, 5]]
#
#     pred = algo.predict_one_csvm(x)
#     data2 = ing.on_actualize_data_dict(4217.45, pred, data2)
#     outliers = ing.detect_outliers(data2)
#     dd = test.make_quick_gen()
#
#     X0 = ing.split_for_sasis(dd)
#     algo.train_one_csvm(X0)
#     predd = algo.predict_one_csvm(X0)
#     d0 = ing.after_train_or_predict_data(dd, predd)
#
#     out0 = ing.detect_outliers(d0)
#     a = out0['2019-07-15':]
#     ing.check_current_prediction(a)
#     print(a['vorhersage'])
#     #ds = db.read_db_content(conn)
#     #print(ds)
