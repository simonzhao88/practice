class Addbook(object):
    def __init__(self, pname=None, phone=None, email=None, dno=None, empno=None):
        self._pname = pname
        self._phone = phone
        self._email = email
        self._dno = dno
        self._empno = empno

    @property
    def pname(self):
        return self._pname

    @property
    def phone(self):
        return self._phone

    @property
    def email(self):
        return self._email

    @property
    def dno(self):
        return self._dno

    @property
    def empno(self):
        return self._empno
