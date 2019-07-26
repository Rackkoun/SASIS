"""book python 3 oop
    https://docs.python.org/3/tutorial/errors.html
"""
class LabelAlreadyExistException(Exception):

    def __init__(self, name_lbl, element = None, message=None):
        super().__init__(name_lbl, message)
        self.name = name_lbl
        self.obj = element
        self.msg = message