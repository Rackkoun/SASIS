"""
    Created on 2019-08-05 at 14:38
    @author: Ruphus
    LOCAL OUTLIER FACTOR-ALGORITHM SKLEARN
"""

from sklearn.neighbors import LocalOutlierFactor


class LocOuFac:

    def __init__(self):
        """
            Der Parameter novelty muss auf True gesetzt werden, um neue Ereignisse vorhersagen zu können
        """
        self.model = LocalOutlierFactor(novelty=True, contamination=.25)
        pass

    def train_locoufac(self, test_data):
        self.model.fit(test_data)

    def predict_locoufac(self, new_daten):
        """
        Mit dieser Methode wird bestimmt, ob es sich um ein Outlier oder nicht handelt
        :param new_daten:
        :return:
        """
        return self.model.predict(new_daten)