# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from DingDianFictionSpider.items import FictionItemLoader, DingdianfictionspiderItem
from DingDianFictionSpider.common import get_md5


class DingdianspiderSpider(scrapy.Spider):
    name = 'DingDianSpider'
    allowed_domains = ['https://www.23us.so/list/5_1.html']
    start_urls = ['https://www.23us.so/list/5_1.html']

    def parse(self, response):
        # 分析朱页面并将一个一个子网页提交请求
        menu_nodes = response.css("table tr[bgcolor='#FFFFFF'] td:nth-child(1) a")
        for fiction_node in menu_nodes:
            fiction_url = fiction_node.css("::attr(href)").extract_first()
            print(fiction_url)
            a = parse.urljoin(response.url, fiction_url)
            print(a)
            yield Request(url=parse.urljoin(response.url, fiction_url), callback=self.parse_html)

        nextpage_url = response.css(".next::attr(href)").extract_first("")
        if nextpage_url:
            yield Request(url=parse.urljoin(response.url, nextpage_url), callback=self.parse)

    def parse_html(self, response):
        item_loader = FictionItemLoader(item=DingdianfictionspiderItem(), response=response)
        item_loader.add_css("title", "head title::text")
        item_loader.add_css("author", "table[bgcolor='#E4E4E4'] tr:nth-child(1) td:nth-child(4)::text")
        item_loader.add_css("category", "table[bgcolor='#E4E4E4'] tr:nth-child(1) td:nth-child(2) a::text")
        item_loader.add_css("word_nums", "table[bgcolor='#E4E4E4'] tr:nth-child(2) td:nth-child(4)::text")
        item_loader.add_css("update_date", "table[bgcolor='#E4E4E4'] tr:nth-child(2) td:nth-child(6)::text")
        item_loader.add_css("content_instrod", ".pl + table + p::text")
        item_loader.add_value("fiction_id", get_md5(response.url))

        fiction_item = item_loader.load_item()

        yield fiction_item
