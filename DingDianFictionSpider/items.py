# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def content_convert(value):
    value = ' '.join(value.split())
    return value


def date_convert(value):
    try:
        value = datetime.datetime.strptime(value.strip(), '%Y-%m-%d %H:%M:%S')
    except Exception as E:
        value = datetime.datetiem.now()
    return value


def title(value):
    if value:
        return '《' + value.split()[0] + '》'
    else:
        return ""


def nums_convert(value):
    try:
        return int(value.strip().strip('字'))
    except:
        return 0


class FictionItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class DingdianfictionspiderItem(scrapy.Item):
    # define the fields for my item here like:
    # name = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(title)
    )
    content_instrod = scrapy.Field(
        input_processor=MapCompose(content_convert)
    )
    author = scrapy.Field()
    word_nums = scrapy.Field(
        input_processor=MapCompose(nums_convert)
    )
    category = scrapy.Field()
    update_date = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    fiction_id = scrapy.Field()
    pass



