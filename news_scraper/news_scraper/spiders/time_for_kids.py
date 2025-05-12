import scrapy
from datetime import datetime
from news_scraper.news_scraper.items import NewsScraperItem

class TimeForKidsSpider(scrapy.Spider):
    name = "time_for_kids"
    allowed_domains = ["timeforkids.com"]
    start_urls = [
        "https://www.timeforkids.com/g34/",
        "https://www.timeforkids.com/k1/",
        "https://www.timeforkids.com/g2/",
        "https://www.timeforkids.com/g56/"
    ]
    page_count = 1  # added page_count attribute

    def parse(self, response):
        # Extract article links from the main page
        article_links = response.css("h2.c-article-preview__title a::attr(href)").getall()  # updated article selector
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        item = NewsScraperItem()
        item["id"] = 7
        item["title"] = response.css("h1.article-show__content-title::text").get(default="").strip()
        item["image_url"] = response.css("div.header_img-wrapper img::attr(src)").get()
        item["content"] = " ".join(response.css("div.article-show__content-article p::text").getall())
        item["source"] = "Time for Kids"
        item["url"] = response.url
        published_text = response.css("h3.article-show__content-date::text").get()
        if published_text:
            try:
                published_date = datetime.strptime(published_text, "%B %d, %Y")
                item["published_at"] = published_date.timestamp()
            except:
                item["published_at"] = datetime.now().timestamp()
        else:
            item["published_at"] = datetime.now().timestamp()
            
        item["is_kid_friendly"] = True
        item["created_at"] = datetime.now().timestamp
        item["categories"] = response.css("ul.article-show__content-sections a::text").getall()
        item["description"] = item["content"].split(".")[0] + "." if "." in item["content"] else item["content"]
        if(item["title"] and item["content"]):
            yield item
