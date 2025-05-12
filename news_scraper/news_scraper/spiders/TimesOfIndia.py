import scrapy
from news_scraper.news_scraper.items import NewsScraperItem
from datetime import datetime
from urllib.parse import urlparse

class TimesofindiaSpider(scrapy.Spider):
    name = "TimesOfIndia"
    allowed_domains = ["timesofindia.indiatimes.com"]
    start_urls = ["https://timesofindia.indiatimes.com"]

    def parse(self, response):
        # Extract category links from the homepage
        category_links = response.css("li.sBgUN.col a::attr(href)").getall()  # Adjust selector as needed

        for link in category_links:
            full_url = response.urljoin(link)
            # Skip "videos" category
            if "videos" not in full_url:
                yield scrapy.Request(url=full_url, callback=self.parse_category)

    def parse_category(self, response):
        # Extract articles from the category page
        articles = response.css("div.col_l_6 figure a::attr(href)").getall()  # Adjust selector as needed

        for article in articles[:5]:
            full_url = response.urljoin(article)
            # Skip "videos" category
            if "videos" not in full_url:
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_article
                )

    def parse_article(self, response):
        # Extract category name from the URL
        parsed_url = urlparse(response.url)
        path_segments = parsed_url.path.strip("/").split("/")
        
        # Assume the category name is the first segment in the URL path
        category_name = path_segments[0] if len(path_segments) > 0 else "Unknown"

        # Skip articles in the "videos" category
        if category_name in ["videos", "city"]:
            return

        # Extract detailed article information
        item = NewsScraperItem()
        item['title'] = response.css("h1.HNMDR span::text").get()  # Adjust selector for article title
        item['url'] = response.url
        item['description'] = response.css("div.M1rHh.undefined::text").get()  # Meta description
        item['content'] = " ".join(response.css("div._s30J.clearfix::text").getall())  # Full article content
        item['image_url'] = response.css("div.wJnIp img::attr(src)").get()  # Featured image
        item['source'] = "Times of India"  # Static source field

        # Extract published date and time
        item['published_at'] = response.css("div.xf8Pm.byline span::text").get()  # Adjust selector for published date
        item['is_kid_friendly'] = False  # Default value
        item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        item['categories'] = [category_name]  # Add the category name extracted from the URL
        if(item['title'] and item['content']):
            yield item