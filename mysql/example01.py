import pymysql


def main():
    # 创建数据库连接（Connection对象）
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        charset='utf8',
        db='hrs'
    )
    try:
        # 创建Cursor对象
        # Cursor对象支持上下文语法可以放在with中
        with conn.cursor() as cursor:
            # 向数据库发送SQL语句
            # execute方法返回受影响的行数
            dno = int(input('部门编号:'))
            dname = input('部门名称:')
            dloc = input('部门地址:')
            # result = cursor.execute('insert into tbdept values (%s, %s, %s)',
            #                         (dno, dname, dloc))
            # result = cursor.execute('insert into tbdept values (%(no)s, %(name)s, %(loc)s)',
            #                         {'no': dno, 'name': dname, 'loc': dloc})
            result = cursor.execute('delete from tbdept where dno=%s', (dno,))
            print(result)
            # 手动提交
            conn.commit()
            print('删除成功' if result == 1 else '删除失败')
    finally:
        conn.close()


if __name__ == '__main__':
    main()
