import scrapy
from news_scraper.news_scraper.items import NewsScraperItem
from datetime import datetime
from urllib.parse import urlparse

class ThehinduSpider(scrapy.Spider):
    name = "TheHindu"
    allowed_domains = ["thehindu.com"]
    start_urls = ["https://www.thehindu.com"]

    def parse(self, response):
        # Extract category links from the specified menu
        category_links = response.css('div.menu-nav a::attr(href)').getall()

        for link in category_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(url=full_url, callback=self.parse_category)

    def parse_category(self, response):
        # Extract articles from the category page
        articles = response.css('h3.title a::attr(href)').getall()  # Adjust selector as needed

        for article in articles[:5]:
            full_url = response.urljoin(article)
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_article
            )

    def parse_article(self, response):
        # Extract category name from the URL
        parsed_url = urlparse(response.url)
        path_segments = parsed_url.path.strip("/").split("/")
        
        # Check if the URL contains "news" and extract the full category name
        if "news" in path_segments:
            category_name = "/".join(path_segments[:2])  # Extract "news/international" or "news/national"
        else:
            category_name = path_segments[0] if len(path_segments) > 1 else "Unknown"

        self.logger.info(f"Extracted Category from URL: {category_name}")  # Debugging log

        # Extract detailed article information
        item = NewsScraperItem()
        item['title'] = response.css("h1.title::text").get().strip()  # Adjust selector for article title
        item['url'] = response.url
        item['description'] = response.css("h2.sub-title::text").get()  # Adjust selector for description
        item['content'] = " ".join(response.css("div.articlebodycontent p::text").getall())  # Full article content
        item['image_url'] = response.css("div.storyline div.article-picture img::attr(src)").get()
        item['source'] = "The Hindu"  # Static source field

        # Extract and clean the published date and time
        published_at_raw = response.css("div.update-publish-time p span::text").get()  # Extract raw text
        if published_at_raw:
            # Extract only the date and time part
            published_at = published_at_raw.split(" - ")[1].strip() if " - " in published_at_raw else published_at_raw.strip()
            item['published_at'] = published_at

        item['is_kid_friendly'] = False  # Default value
        item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        item['categories'] = [category_name]  # Add the category name extracted from the URL
        if(item['title'] and item['content']):
            yield item