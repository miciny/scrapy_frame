# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import json
from concurrent.futures import ThreadPoolExecutor
from spider.utils.SaveDataToDB import save


class SpiderPipeline:
    def process_item(self, item, spider):
        key_word = ['python', 'py', '爬虫', '抢购', '小程序', '项目', '数据', 'vue', '网站']
        check_str = item['title'].lower()
        if "已完成" in item['status']:
            raise DropItem("==================== %s: 已完成" % check_str)

        if "已重置" in item['content']:
            raise DropItem("==================== %s: 已重置" % check_str)

        if any(ext in check_str for ext in key_word):
            print("==================== %s: 包含关键词" % check_str)
            return item
        else:
            raise DropItem("==================== %s: 不包含关键字" % check_str)


class SavePipeline:
    def __init__(self):
        # 打开文件
        self.file = open('data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        title = item['title']
        print("==================== 数据保存: %s" % title)
        # 读取item中的数据
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 写入文件
        self.file.write(line)

        with ThreadPoolExecutor() as t:
            t.submit(save, item)

        return item


class ImgPipeline(ImagesPipeline):
    # 通过抓取的图片url获取一个Request用于下载
    def get_media_requests(self, item, info):
        # 返回Request根据图片图片url下载
        icon_url = item['icon_url']
        print("==================== 图片下载: %s" % icon_url)
        yield scrapy.Request(icon_url)

    # 当下载请求完成后执行该方法
    def item_completed(self, results, item, info):
        # 获取下载地址
        image_path = [x['path'] for ok, x in results if ok]
        title = item['title']
        # 判断是否成功
        if not image_path:
            print("==================== %s 图片下载失败: %s" % (title, image_path))
            image_path = "图片下载失败"
        # 将地址存入item
        print("==================== %s 图片下载成功: %s" % (title, image_path))
        item['icon_path'] = image_path

        return item
