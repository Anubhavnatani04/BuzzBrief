import scrapy
from datetime import datetime
from news_scraper.news_scraper.items import NewsScraperItem
from dateutil.parser import parse

class RobinageSpider(scrapy.Spider):
    name = "Robinage"
    allowed_domains = ["www.robinage.com"]
    start_urls = ["https://www.robinage.com/category/news-for-kids/india-news/", "https://www.robinage.com/category/news-for-kids/world-news/", "https://www.robinage.com/category/news-for-kids/space-science/"]

    def parse(self, response):
        # Extract article links using assumed selectors
        links = response.css("div.magazine-posts a::attr(href)").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        item = NewsScraperItem()
        item["categories"] = response.css("a.cat-link::text").getall()
        item["title"] = response.css("div.title-caption h1::text", ).get(default="").strip()
        if("India News" in item["categories"]):
            item["content"] = " ".join(response.css("li.p1 *::text").getall())
        else:
            item["content"] = " ".join(response.css("p.p1 *::text").getall())
        item["image_url"] = response.css("img.post-thumbnail::attr(src)").get()

        # Handle date conversion
        published_text = response.css("div.elementor-widget-container h6::text").get()
        if published_text:
            try:
                published_date = parse(published_text.strip())
                item["published_at"] = published_date.timestamp()
            except:
                item["published_at"] = datetime.now().timestamp()
        else:
            item["published_at"] = datetime.now().timestamp()

        item["source"] = "Robinage"
        item["url"] = response.url
        item["is_kid_friendly"] = True
        item["created_at"] = datetime.now().timestamp()
        
        description = item["content"].split(".")[0] + "." if "." in item["content"] else item["content"]
        item["description"] = description
        if(item["title"] and item["content"]):
            yield item
