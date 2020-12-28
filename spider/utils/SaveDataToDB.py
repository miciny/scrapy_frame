from spider.utils.MySqlPool import MySqlPool
from concurrent.futures import ThreadPoolExecutor
from spider import mcy_setting
import json


def read():
    with open("D:\GitHub\Python\scrapy\spider\data.json", 'r', encoding='utf-8') as f:
        with ThreadPoolExecutor() as t:
            for line in f.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                t.submit(save, json.loads(line))


def save(item):
    sql_handler = MySqlPool(db="worm")

    try:
        sql = "select count(1) from work_spider where url='%s'" % item['target_url']
        res = sql_handler.select_sql(sql)
        if res and res[0][0] > 0:
            return

        sql = ("insert into work_spider (title, content, url, take_time, salary, create_time) values "
               "('%s', '%s', '%s', '%s', '%s', NOW())" %
               (item['title'], item['content'], item['target_url'], item['time'], item['price']))
        # print("保存成功：", str(item['title']))
        mcy_setting.add_no += 1
        return sql_handler.other_sql(sql)
    finally:
        sql_handler.close_conn()


if __name__ == '__main__':
    read()
