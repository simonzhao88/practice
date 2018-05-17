import pymysql
from example03 import Dept


def main():
    # 创建数据库连接（Connection对象）
    # conn = pymysql.connect(
    #     host='localhost',
    #     port=3306,
    #     user='root',
    #     password='root',
    #     charset='utf8',
    #     db='hrs',
    #     cursorclass=pymysql.cursors.DictCursor
    # )
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'charset': 'utf8',
        'db': 'hrs',
        'cursorclass': pymysql.cursors.DictCursor
    }
    conn = pymysql.connect(**config)
    try:
        # 创建Cursor对象
        # Cursor对象支持上下文语法可以放在with中
        with conn.cursor() as cursor:
            # 向数据库发送SQL语句
            # execute方法返回受影响的行数
            cursor.execute('select dno, dname, dloc from tbdept')
            result = cursor.fetchone()
            while result:
                # 关系型数据库  - 关系模型
                # Python程序  - 对象模型
                # ORM  - Objiect Relation Mapping
                # Alchemy
                # 有了ORM以后操作数据库就在也不用写SQL
                dept = Dept(**result)
                print(dept.name)
                result = cursor.fetchone()
                # 手动提交
    except BlockingIOError:
        # 如果事务中的所有操作全部都成功了最后手动提交事务
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
