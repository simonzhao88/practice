import pymysql
from addbook import Addbook


class Mysqlhandler(object):
    def __init__(self, host, port, user, passwd, db):
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._db = db
        self._charset = 'utf8'

    def conn(self):
        conn = pymysql.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._passwd,
            charset='utf8',
            db=self._db,
        )
        return conn

    def insert(self, values=None):
        conn = self.conn()
        try:
            with conn.cursor() as cursor:
                if isinstance(values, tuple):
                    # sql = 'insert into addressbook (pname, phone, email, dno, empno) values {}'.format(values)
                    result = cursor.execute('insert into addressbook (pname, phone, email, dno, empno) values {}'
                                            .format(values))
                    conn.commit()
                    print('新增成功，%d行受影响~~' % result)
        except:
            print('出错了~~')
        finally:
            conn.close()

    def update(self, args=None, pname=None):
        conn = self.conn()
        try:
            with conn.cursor() as cursor:
                if isinstance(args, str):
                    # sql = 'update addressbook set {0} where pname="{1}"'.format(args, pname)
                    # print(sql)
                    cursor.execute('update addressbook set {0} where pname="{1}"'.format(args, pname))
                    conn.commit()
                    print('修改联系人成功~~')
        finally:
            conn.close()

    def delete(self, pname=None):
        conn = self.conn()
        try:
            with conn.cursor() as cursor:
                # sql = 'delete from addressbook where pname="{}"'.format(pname)
                cursor.execute('delete from addressbook where pname="{}"'.format(pname))
                conn.commit()
                print('联系人删除成功~')
        finally:
            self.conn().close()

    def select(self, pname=None):
        conn = self.conn()
        try:
            with conn.cursor() as cursor:
                if pname is None:
                    # sql = 'select pname, phone, email, dno, empno from addressbook'
                    results = cursor.execute('select pname, phone, email, dno, empno from addressbook')
                    if results != 0:
                        results = cursor.fetchall()
                        for result in results:
                            addbook = Addbook(*result)
                            tab = ' ' * 6
                            print('姓名', tab, '电话', tab, '邮箱', tab, '部门编号', tab, '员工编号')
                            print('%s      %s      %s       %d       %d'.ljust(10, ' ')
                                  % (addbook.pname, addbook.phone, addbook.email, addbook.dno, addbook.empno))
                    else:
                        print('没有查到联系人~~')
                else:
                    # sql = 'select pname, phone, email, dno, empno from addressbook where pname="{}"'.format(pname)
                    result = cursor.execute('select pname, phone, email, dno, empno from addressbook where pname="{}"'
                                            .format(pname))
                    if result != 0:
                        result = cursor.fetchone()
                        addbook = Addbook(*result)
                        tab = ' ' * 6
                        print('姓名', tab, '电话', tab, '邮箱', tab, '部门编号', tab, '员工编号')
                        print('%s      %s      %s       %d       %d'.ljust(10, ' ')
                              % (addbook.pname, addbook.phone, addbook.email, addbook.dno, addbook.empno))
                    else:
                        print('没有查到联系人~~')
        finally:
            conn.close()
