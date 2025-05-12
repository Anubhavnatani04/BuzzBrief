import scrapy
from datetime import datetime
from news_scraper.news_scraper.items import NewsScraperItem
from dateutil.parser import parse

class ChildrenspostSpider(scrapy.Spider):
    name = "ChildrensPost"
    allowed_domains = ["kidsnews.top"]
    start_urls = ["https://kidsnews.top/category/newsforkids/"]

    def parse(self, response):
        page_count = response.meta.get('page_count', 1)
        links = response.css("main.site-main a::attr(href)").getall()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_post)
        next_page = response.css("a.next::attr(href)").get()
        if next_page and page_count < 3:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse,
                meta={'page_count': page_count + 1}
            )

    def parse_post(self, response):
        item = NewsScraperItem()
        item['url'] = response.url
        item['title'] = response.css("h1.entry-title::text").get(default="").strip()
        content = " ".join(response.css("div.entry-content p::text").getall()).strip()
        item['content'] = content
        item['image_url'] = response.css("div.entry-content img::attr(src)").get()
        item['source'] = "The Childrens Post Of India"
        
        # Convert date string to timestamp
        date_str = response.css("span.posted-on a::text").get()
        if date_str:
            try:
                published_date = parse(date_str)
                item['published_at'] = published_date.timestamp()
            except:
                item['published_at'] = datetime.now().timestamp()
        else:
            item['published_at'] = datetime.now().timestamp()
            
        item['is_kid_friendly'] = True
        item['created_at'] = datetime.now().timestamp()
        item['categories'] = response.css("span.cats-links a::text").getall()
        if '.' in content:
            item['description'] = content.split('.', 1)[0] + '.'
        else:
            item['description'] = content
        if(item['title'] and item['content']):
            yield item
