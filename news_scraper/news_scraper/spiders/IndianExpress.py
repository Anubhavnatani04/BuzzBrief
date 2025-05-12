import scrapy
from news_scraper.news_scraper.items import NewsScraperItem
from datetime import datetime
from urllib.parse import urlparse

class IndianexpressSpider(scrapy.Spider):
    name = "IndianExpress"
    allowed_domains = ["indianexpress.com"]
    start_urls = ["https://indianexpress.com"]

    def parse(self, response):
        # Extract category links from the homepage
        category_links = response.css('div.mainnav a::attr(href)').getall()  # Adjust selector as needed

        for link in category_links:
            full_url = response.urljoin(link)
            # Pass the category name to the next request
            yield scrapy.Request(url=full_url, callback=self.parse_category)

    def parse_category(self, response):
        # Extract articles from the category page
        articles = response.css("div.top-news h3 a::attr(href)").getall()  # Adjust selector as needed

        for article in articles[:5]:  # Limit to 5 articles per category
            full_url = response.urljoin(article)
            # Pass the article URL to the next request
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_article
            )

    def parse_article(self, response):
        # Extract category name from the URL
        parsed_url = urlparse(response.url)
        path_segments = parsed_url.path.strip("/").split("/")
        
        # Extract the category name after the word "article"
        if "article" in path_segments:
            article_index = path_segments.index("article")
            category_name = path_segments[article_index + 1] if article_index + 1 < len(path_segments) else "Unknown"
        else:
            category_name = "Unknown"

        # Extract detailed article information
        item = NewsScraperItem()
        item['title'] = response.css("div.heading-part h1::text").get()  # Adjust selector for article title
        item['url'] = response.url
        item['description'] = response.css("h2.synopsis::text").get()  # Adjust selector for description
        item['content'] = " ".join(response.css("div.story_details p::text").getall())  # Full article content
        item['image_url'] = response.css("span.custom-caption img::attr(src)").get()  # Featured image
        item['source'] = "Indian Express"  # Static source field

        # Extract and clean the published date and time
        published_at_raw = response.css("div#storycenterbyline span::text").get()  # Extract raw text
        if published_at_raw:
            # Remove "Updated:" and clean the date and time
            published_at = published_at_raw.replace("Updated:", "").strip()
            item['published_at'] = published_at

        item['is_kid_friendly'] = False  # Default value
        item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        item['categories'] = [category_name]  # Add the category name extracted from the URL
        if(item['title'] and item['content']):
            yield item