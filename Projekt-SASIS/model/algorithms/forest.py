"""
    Created on 2019-08-05 at 14:25
    @author: Ruphus
    ISOALTION FOREST-ALGORITHM SKLEARN
"""

from sklearn.ensemble import IsolationForest


class IsolFo:

    def __init__(self):
        self.model = IsolationForest(n_estimators=25, max_samples=75, random_state=0, contamination=.25,
                                     behaviour='new',
                                     warm_start=True)
        pass

    def train_isolfo(self, test_data):
        self.model.fit(test_data)
        self.model.set_params(n_estimators=30) # beutze die Info auf dem vorherigen Training
        self.model.fit(test_data) # dann trainiert wieder

    def predict_isolfo(self, new_daten):
        """
        Mit dieser Methode wird bestimmt, ob es sich um ein Outlier oder nicht handelt
        :param new_daten:
        :return:
        """
        return self.model.predict(new_daten)