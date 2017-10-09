# -*- coding: utf-8 -*-
import scrapy
from dongguan.items import DongguanItem


class SunSpider(scrapy.Spider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page={offset}'
    offset = 0
    start_urls = [url.format(offset=offset)]

    def parse(self, response):
        links = response.xpath("//div[@class='greyframe']/table//td/a[@class='news14']/@href").extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)
        if self.offset <= 81030:
            self.offset += 30
            yield scrapy.Request(self.url.format(offset=self.offset), callback=self.parse)

    def parse_item(self, response):
        item = DongguanItem()
        # 标题
        item['title'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract()[0]

        # 编号
        item['number'] = item['title'].split(' ')[-1].split(":")[-1]

        # 文字内容，默认先取出有图片情况下的文字内容列表
        content = response.xpath('//div[@class="contentext"]/text()').extract()
        # 如果没有内容，则取出没有图片情况下的文字内容列表
        if len(content) == 0:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
            # content为列表，通过join方法拼接为字符串，并去除首尾空格
            item['content'] = "".join(content).strip()
        else:
            item['content'] = "".join(content).strip()

        # 链接
        item['url'] = response.url

        yield item
