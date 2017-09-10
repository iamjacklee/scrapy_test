# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector
from cnblogSpider.items import CnblogspiderItem

class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls =['http://www.cnblogs.com/qiyeboy/default.html?page=1']

    def parse(self,response):
        papers = response.xpath('.//*[@class="day"]')

        for paper in papers:
            url = paper.xpath('.//div[@class="postTitle"]/a/@href').extract()[0]
            title = paper.xpath('.//div[@class="postTitle"]/a/text()').extract()[0]
            time = paper.xpath('.//div[@class="dayTitle"]/a/text()').extract()[0]
            content = paper.xpath('.//div[@class="c_b_p_desc"]/text()').extract()[0]
            # print '\n'
            # print title,url,time,content
            item = CnblogspiderItem(url=url,title=title,time=time,content=content)
            yield item

        next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
        if next_page:
            yield scrapy.Request(url=next_page[0],callback=self.parse)

        # next_page = Selector(response).re(u'<a href="(\S*)">下一页</a>')
        # if next_page:
        #     yield scrapy.Request(url=next_page[0], callback=self.parse)
