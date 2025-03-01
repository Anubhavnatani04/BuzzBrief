# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScraperItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    image_url = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    published_at = scrapy.Field()
    is_kid_friendly = scrapy.Field()
    created_at = scrapy.Field()  # Timestamp of record creation
    categories = scrapy.Field()  # New field: holds list of categories
    description = scrapy.Field()  # New field: holds article description
