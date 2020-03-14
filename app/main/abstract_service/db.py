import pymysql
import pprint


# 持久层

def get_conn():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='12345678',
        database='auto_abstract',
        charset='utf8'
    )


def query_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


def query_data_with_param(sql, param):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, param)
        return cursor.fetchall()
    finally:
        conn.close()


def insert_or_update_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        ret = cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
        return ret


# 新增blob数据，避免sql注入问题
def insert_with_param(sql, param):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        # 成功自动返回1
        ret = cursor.execute(sql, param)
        conn.commit()
        if ret == 1:
            print("insert successfully.")
            cursor.execute("select LAST_INSERT_ID()")
            return cursor.fetchall()
        else:
            return 0
    # except Exception:
        # print("error")
        # return 0
    finally:
        conn.close()


if __name__ == '__main__':
    sql = "insert user (name, sex, age, email) values ('John', 'man', 30, 'John@gmail.com')"
    # insert_or_update_data(sql)
    sql = "select * from sgrade"
    data = query_data(sql)
    pprint.pprint(data)
