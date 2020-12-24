import pymysql  # 数据库连接
from dbutils.pooled_db import PooledDB  # 用于数据库连接池
import traceback

"""
数据库配置
"""
mysql_ip = '39.105.72.114'
mysql_port = '3306'
mysql_user = 'root'
mysql_pw = 'Miciny219219'


class MySqlPool:

    sql_dict = dict()
    sql_config = dict()

    def __init__(self, db, info_dict=None, t_no=1):
        if info_dict:
            db_host = info_dict['host']
        else:
            db_host = mysql_ip
        sql_key = db_host+str(db)

        if sql_key not in MySqlPool.sql_dict.keys():
            if info_dict:
                db_user = info_dict['username']
                db_pwd = info_dict['password']
                db_port = info_dict['port']
            else:
                db_user = mysql_user
                db_pwd = mysql_pw
                db_port = mysql_port

            MySqlPool.sql_config = {
                "host": db_host,
                "port": int(db_port),
                "user": db_user,
                "password": db_pwd,
                "database": db
            }

            print("连接数据库：", db_host, db_port, db_user, db_pwd, db)
            POOL = PooledDB(
                pymysql,
                t_no,                  # 连接池里的最少连接数
                **MySqlPool.sql_config
            )
            MySqlPool.sql_dict[sql_key] = POOL
        else:
            print("已连接数据库：", db_host, db)

        self.sql_pool = MySqlPool.sql_dict[sql_key]
        self.conn = self.sql_pool.connection()
        self.cursor = self.conn.cursor()  # 创建游标

    # 查询
    def select_sql(self, sql_str):
        try:
            self.cursor.execute(sql_str)
            print("执行成功：", sql_str)
            print("结果数量：", self.cursor.rowcount)
            print("表字段名称：")
            data_dict = list()
            for field in self.cursor.description:
                data_dict.append(field[0])
            print(data_dict)
            rs = self.cursor.fetchall()
            if self.cursor.rowcount > 0:
                for r in rs:
                    if len(str(r)) < 500:
                        print(r)
            return rs
        except Exception as ex:
            print("执行失败：", sql_str)
            print("失败原因：", ex)
            print(traceback.format_exc())
            return None
        finally:
            print("======>>>>>>\n")

    # "增删改"
    def other_sql(self, sql_str):
        try:
            self.cursor.execute(sql_str)
            print("执行成功：", sql_str)
            print("受影响行数：", self.cursor.rowcount)
            self.conn.commit()  # "增删改" 之后，还需要执行commit()
            return True
        except Exception as ex:
            print("执行失败：", sql_str)
            print("失败原因：", ex)
            self.conn.rollback()
            return False
        finally:
            print("======>>>>>>\n")

    def close_conn(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    test = MySqlPool(db="mcy_platform")
    sql = "SELECT * FROM user_info;"
    test.select_sql(sql)
    test.close_conn()
