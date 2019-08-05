"""
    Created on 2019-08-05 at 14:38
    @author: Ruphus
    ONE CLASS SVM-ALGORITHM SKLEARN
"""

from sklearn.svm import OneClassSVM


class OneCSVM:

    def __init__(self):
        self.model = OneClassSVM(nu=.3, gamma='scale')
        pass

    def train_one_csvm(self, test_data):
        self.model.fit(test_data)

    def predict_one_csvm(self, new_daten):
        """
        Mit dieser Methode wird bestimmt, ob es sich um ein Outlier oder nicht handelt
        :param new_daten:
        :return:
        """
        return self.model.predict(new_daten)