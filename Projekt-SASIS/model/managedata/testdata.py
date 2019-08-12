"""
    Created on 05.08.2019 at 13:59
    @author: Ruphus
    Erzeuge Daten zum Testen des Programm. Des Weiteren diesen auch die generierten Daten als
    Training für das System (für diese Version)
    source date: https://stackoverflow.com/questions/30483977/python-get-yesterdays-date-as-a-string-in-yyyy-mm-dd-format/30484112
"""

import pandas as pd
import numpy as np


class TestDataGenerator:
    SEED = np.random.seed(0)  # global Zufallgenerator

    def __init__(self):
        self.std = 4019.59 + 4019.59 * .3
        self.data = None
        pass

    def gen_date(self, start, end, freq):
        return pd.date_range(start=start, end=end, freq=freq)

    def on_generate(self, n_samples):
        return np.random.random(size=n_samples)

    def on_normalize(self, data, error):
        return np.random.normal(((self.std - 1.) / (data + 1.)), error)

    def on_create_test_data(self, start_date, en_date, date_periode, error):
        datum = self.gen_date(start_date, en_date, date_periode)
        genval = self.on_generate(len(datum))
        data = self.on_normalize(genval, error)

        df = pd.DataFrame(columns=['strom', 'tag', 'monat', 'jahr', 'wochentag'], index=datum)
        df['strom'] = data
        df['tag'] = df.index.day
        df['monat'] = df.index.month
        df['jahr'] = df.index.year
        df['wochentag'] = df.index.weekday_name

        return df

    def make_quick_gen(self):
        quick_gen = self.on_create_test_data(start_date='2019-04-01', en_date='2019-08-01', date_periode='D', error=.3)
        return quick_gen

    def split_for_ml_test(self, df):
        X1 = df.iloc[:, [0, 1]].values

        return X1
