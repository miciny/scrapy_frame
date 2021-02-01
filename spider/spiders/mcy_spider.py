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
        base_xpath = '//div[@class="weui_panel weui_panel_access weui_panel_access_adapt db_adapt margin-top-2 "]'
        for box in response.xpath(base_xpath):
            try:
                item['title'] = box.xpath('.//div[@class="topic_title"]/text()').extract()[0]
                item['content'] = box.xpath('.//p[@class="media_desc_adapt "]/text()').extract()[0]
                item['name'] = box.xpath('.//h4[@class="weui_media_title font-color-3"]/text()').extract()[0]
                item['icon_url'] = box.xpath('.//img[@class="weui_media_appmsg_thumb radius_img_50"]/@src').extract()[0]
                item['target_url'] = box.xpath('.//a[1]/@href').extract()[0]
                item['status'] = box.xpath('.//a[contains(@id, "appoint_job_")]/text()').extract()[0]
                item['price'] = box.xpath('.//span[@class="rixin-text-jobs"]/text()').extract()[0] + \
                                box.xpath('.//span[@class="rixin-text-jobs"]/span/text()').extract()[0]
                item['time'] = box.xpath('.//p[@class="media_desc_adapt"]/span[3]/text()').extract()[0] + \
                               box.xpath('.//p[@class="media_desc_adapt"]/span[3]/span/text()').extract()[0]
            except Exception as e:
                print(e)
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
