import scrapy
from spider.items import SpiderItem
import copy


class McySpider(scrapy.Spider):
    name = 'mcy_spider'
    allowed_domains = ['www.yuanjisong.com']
    start_urls = ['https://www.yuanjisong.com/job']

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
                item['price'] = box.xpath('.//span[@class="rixin-text-jobs"]/text()').extract()[0] + \
                                box.xpath('.//span[@class="rixin-text-jobs"]/span/text()').extract()[0]
                item['time'] = box.xpath('.//p[@class="media_desc_adapt"]/span[3]/text()').extract()[0] + \
                               box.xpath('.//p[@class="media_desc_adapt"]/span[3]/span/text()').extract()[0]
            except Exception as _:
                item['title'] = "无内容"
                item['content'] = "无内容"
                item['name'] = "无内容"
                item['icon_url'] = "无内容"
                item['price'] = "无内容"
                item['time'] = "无内容"
                item['target_url'] = "无内容"
            # 返回信息  Request 函数传递 item 时，使用的是浅复制,图片下载的话，会有问题
            yield copy.deepcopy(item)

        # url跟进开始
        # 获取下一页的url信息
        url = response.xpath("//a[contains(text(),'下一页')]/@href").extract()
        if url:
            page = url[0]
            # 返回url
            yield scrapy.Request(page, callback=self.parse)
