import scrapy
from news_scraper.items import NewsScraperItem
from datetime import datetime

class ChildrenspostSpider(scrapy.Spider):
    name = "ChildrensPost"
    allowed_domains = ["kidsnews.top"]
    start_urls = ["https://kidsnews.top/category/newsforkids/"]

    def parse(self, response):
        page_count = response.meta.get('page_count', 1)
        # Extract article links using CSS selectors (assumed structure)
        links = response.css("main.site-main a::attr(href)").getall()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_post)
        # Handle pagination if available, limit to 3 pages
        next_page = response.css("a.next::attr(href)").get()
        if next_page and page_count < 3:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse,
                meta={'page_count': page_count + 1}
            )

    def parse_post(self, response):
        # Parse the article detail page
        item = NewsScraperItem()
        item['url'] = response.url
        item['title'] = response.css("h1.entry-title::text").get(default="").strip()
        content = " ".join(response.css("div.entry-content p::text").getall()).strip()
        item['content'] = content
        item['image_url'] = response.css("div.entry-content img::attr(src)").get()
        item['source'] = "The Childrens Post Of India"
        item['published_at'] = response.css("span.posted-on a::text").get()
        item['is_kid_friendly'] = True
        item['created_at'] = datetime.now().isoformat()
        item['categories'] = response.css("span.cats-links a::text").getall()
        # derive description from content up to first period
        if '.' in content:
            item['description'] = content.split('.', 1)[0] + '.'
        else:
            item['description'] = content
        if(item['title'] and item['content']):
            yield item
