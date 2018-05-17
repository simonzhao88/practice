class Dept(object):

    def __init__(self, dno=None, dname=None, dloc=None):
        self._no = dno
        self._name = dname
        self._loc = dloc

    @property
    def no(self):
        return self._no

    @property
    def name(self):
        return self._name

    @property
    def loc(self):
        return self._loc