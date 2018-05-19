from mysqlhandler import Mysqlhandler


class Address(object):
    def __init__(self):
        self._host = 'localhost'
        self._port = 3306
        self._user = 'root'
        self._passwd = 'root'
        self._db = 'hrs'
        self._connect = Mysqlhandler(
            self._host, self._port, self._user, self._passwd, self._db)

    def insert(self):
        pname = input('请输入员工姓名：')
        phone = input('请输入员工电话：')
        email = input('请输入员工邮箱：')
        dno = int(input('请输入员工部门编号：'))
        empno = int(input('请输入员工编号：'))
        self._connect.insert(values=(pname, phone, email, dno, empno))

    def show(self):
        pname = input('请输入要查询的联系人姓名：')
        self._connect.select(pname=pname)

    def showall(self):
        self._connect.select()

    def modify(self):
        pname = input('请输入要修改的联系人姓名：')
        print('电话：1 邮箱：2 部门编号：3 员工编号：4 完成修改：9')
        md = True
        values = ''
        while md:
            type = int(input('请选择要修改的项：'))
            if type == 9:
                md =False
            elif type == 1:
                value1 = input('请输入修改的数据：')
                values += 'phone=' + value1 + ','
            elif type == 2:
                value2 = input('请输入修改的数据：')
                values += 'email=' + value2 + ','
            elif type == 3:
                value3 = input('请输入修改的数据：')
                values += 'dno=' + value3 + ','
            elif type == 4:
                value4 = input('请输入修改的数据：')
                values += 'empno=' + value4 + ','
        values = values[0:-1]
        self._connect.update(pname=pname, args=values)

    def delete(self):
        pname = input('请输入要删除的联系人姓名：')
        self._connect.delete(pname=pname)


def main():
    print('欢迎登陆通讯录系统~~')
    print('查看全部联系人：1')
    print('查看联系人：2')
    print('新增联系人：3')
    print('修改联系人：4')
    print('删除联系：5')
    print('退出系统：0')
    login = True
    while login:
        control = int(input('请输入操作代号：'))
        if control == 1:
            showall = Address()
            showall.showall()
        elif control == 2:
            show = Address()
            show.show()
        elif control == 3:
            insert = Address()
            insert.insert()
        elif control == 4:
            modify = Address()
            modify.modify()
        elif control == 5:
            delete = Address()
            delete.delete()
        elif control == 0:
            print('Bye~Bye~')
            login = False


if __name__ == '__main__':
    main()
