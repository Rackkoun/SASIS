"""
    Created on 2019-08-05 at 14:37
    @author: Ruphus
    ELLIPTIC-ENVELOPE-ALGORITHM SKLEARN
"""

from sklearn.covariance import EllipticEnvelope


class EllipticEnv:

    def __init__(self):
        self.model = EllipticEnvelope(random_state=0, contamination=.15)
        pass

    def train_ellipenv(self, test_data):
        self.model.fit(test_data)

    def predict_ellipenv(self, new_daten):
        """
        Mit dieser Methode wird bestimmt, ob es sich um ein Outlier oder nicht handelt
        :param new_daten:
        :return:
        """
        return self.model.predict(new_daten)