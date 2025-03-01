import scrapy
from datetime import datetime
from news_scraper.items import NewsScraperItem

class MintSpider(scrapy.Spider):
    name = "Mint"
    allowed_domains = ["www.livemint.com"]
    start_urls = ["https://www.livemint.com/latest-news/page-1"]

    def parse(self, response):
        links = response.css("h2.headline a::attr(href)").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_article)
    
    def parse_article(self, response):
        item = NewsScraperItem()
        # Extract title from h1 (update selector if needed)
        item["title"] = response.css("h1#article-0::text").get(default="").strip()
        # Extract and clean content
        content = "\n".join(response.css("div.storyPage_storyContent__m_MYl")[0].css("*::text").getall()).strip()
        # Remove ad-related content
        item["content"] = content
        # Retrieve image URL, if present
        item["image_url"] = response.css("div.storyPage_storyBox__zPlkE img::attr(src)").get()
        # Extract published date from an assumed element; adjust selector as needed
        item["published_at"] = response.css("div.storyPage_date__JS9qJ span::text").get(default="").strip().split(",")[0]
        # Set static/required fields
        item["source"] = "Mint"
        item["url"] = response.url
        item["is_kid_friendly"] = False
        item["created_at"] = datetime.now()
        # Extract categories (if available)
        item["categories"] = 'General'
        if '.' in content:
            item['description'] = content.split('.', 1)[0] + '.'
        else:
            item['description'] = content
        # Ensure title and content are not empty
        if item["title"] and item["content"]:
            yield item
