# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging

class NewsScraperPipeline:
    def process_item(self, item, spider):
        logging.info(f"Processing item: {item}")
        return item

class CollectorPipeline:
    """Pipeline to collect items and pass them to callback"""
    
    def process_item(self, item, spider):
        if hasattr(spider, 'parse_item'):
            spider.parse_item(item)
        return item
