import scrapy
from news_scraper.news_scraper.items import NewsScraperItem
from datetime import datetime
from urllib.parse import urlparse

class ThestatesmanSpider(scrapy.Spider):
    name = "TheStatesman"
    allowed_domains = ["thestatesman.com"]
    start_urls = ["https://thestatesman.com"]

    def parse(self, response):
        # Extract category links from the homepage
        category_links = response.css("ul.main-menu.d-none.d-lg-inline li a::attr(href)").getall()  # Adjust selector as needed

        for link in category_links:
            full_url = response.urljoin(link)
            # Skip "videos" and "photos" categories
            if "videos" not in full_url and "photo" not in full_url:
                yield scrapy.Request(url=full_url, callback=self.parse_category)

    def parse_category(self, response):
        # Extract article links from the category page
        articles = response.css("h6.post-title.font-weight-bold.mb-10 a::attr(href)").getall()  # Adjust selector as needed

        for article in articles:
            full_url = response.urljoin(article)
            yield scrapy.Request(url=full_url, callback=self.parse_article)

        # Handle pagination
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            full_next_page = response.urljoin(next_page)
            yield scrapy.Request(url=full_next_page, callback=self.parse_category)

    def parse_article(self, response):
        # Extract category name from the URL
        parsed_url = urlparse(response.url)
        path_segments = parsed_url.path.strip("/").split("/")
        category_name = path_segments[0] if len(path_segments) > 0 else "Unknown"

        # Skip articles in the "videos" and "photos" categories
        if category_name in ["videos", "videogallery", "photo", "photos", "supplements"]:
            return        

        # Extract detailed article information
        item = NewsScraperItem()
        item['title'] = response.css("h1.entry-title::text").get().strip()  # Adjust selector for article title
        item['url'] = response.url
        item['description'] = response.css("div.entry-header.mb-30.mt-50 p::text").get()  # Meta description
        item['content'] = " ".join(response.css("div.entry-main-content p::text").getall()).strip()  # Full article content

        # Extract image URL and filter for .webp images
        item['image_url'] = response.css("figure.image img::attr(src)").get()
        item['source'] = "The Statesman"  # Static source field

        # Extract published date and time
        item['published_at'] = response.css("span.post-date::text").get()  # Extract raw text
        item['is_kid_friendly'] = False  # Default value
        item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        item['categories'] = [category_name]  # Add the category name extracted from the URL
        yield item
