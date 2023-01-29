import scrapy
from spider.items import SpiderItem
from spider import mcy_setting
from spider.utils.WechatServices import send_wechat_notice
import copy


class McySpider(scrapy.Spider):
    name = 'mcy_spider'
    allowed_domains = ['www.yuanjisong.com']
    start_urls = ['https://www.yuanjisong.com/job']
    the_times = mcy_setting.times

    def parse(self, response):
        item = SpiderItem()
        base_xpath = '//div[@class="consultant_title margin_top_15"]'
        for box in response.xpath(base_xpath):
            try:
                item['title'] = box.xpath('.//dd[@class="text_type_1 line_clamp_1  float_l line_height_16 "]/b/text()').extract()[0]  #
                print(f"item['title']: {item['title']}")

                item['content'] = box.xpath('.//p[@class="margin_bottom_10"]/text()').extract()[0] #
                print(f"item['content']: {item['content']}")

                item['name'] = box.xpath('.//a[@class="font-size-1 margin_left_1"]/span/text()').extract()[0]  #
                print(f"item['name']: {item['name']}")

                item['icon_url'] = box.xpath('.//img[@class="border_radius_2 width_height_3 float_l"]/@src').extract()[0]  #
                print(f"item['icon_url']: {item['icon_url']}")

                item['target_url'] = box.xpath('.//a[1]/@href').extract()[0]  #
                print(f"item['target_url']: {item['target_url']}")

                item['status'] = box.xpath('.//a[contains(@id, "appoint_job_")]/text()').extract()[0]  #
                print(f"item['status']: {item['status']}")

                item['price'] = box.xpath('.//span[@class="rixin-text-jobs font-size-8 margin-r-2"]/text()').extract()[0] + "元"  #
                print(f"item['price']: {item['price']}")

                item['time'] = box.xpath('.//p[2]/span[3]/text()').extract()[0] + "天"  #
                print(f"item['time']: {item['time']}")

            except Exception as e:
                print(f"出错： {e}")
                item['title'] = "无内容"
                item['content'] = "无内容"
                item['name'] = "无内容"
                item['icon_url'] = "无内容"
                item['price'] = "无内容"
                item['time'] = "无内容"
                item['target_url'] = "无内容"
                item['status'] = "无内容"
                # 返回信息  Request 函数传递 item 时，使用的是浅复制,图片下载的话，会有问题
            yield copy.deepcopy(item)

        # url跟进开始
        # 获取下一页的url信息
        url = response.xpath("//a[contains(text(),'下一页')]/@href").extract()
        self.the_times -= 1
        if url and self.the_times > 0:
            page = url[0]
            # 返回url
            yield scrapy.Request(page, callback=self.parse)

    # 爬虫结束时执行的函数
    def closed(self, reason):
        out_str = '更新数据：%s' % mcy_setting.add_no
        send_wechat_notice("工作检查爬虫", out_str)
        print(out_str)
