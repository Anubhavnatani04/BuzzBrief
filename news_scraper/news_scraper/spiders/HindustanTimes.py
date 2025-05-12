import scrapy
from news_scraper.news_scraper.items import NewsScraperItem
from datetime import datetime
from urllib.parse import urlparse

class HindustantimesSpider(scrapy.Spider):
    name = "HindustanTimes"
    allowed_domains = ["hindustantimes.com"]
    start_urls = ["https://hindustantimes.com"]

    def parse(self, response):
        # Extract category links from the homepage
        category_links = response.css("li.collapse.mTop div a::attr(href), li.collapse div a::attr(href)").getall()

        for link in category_links:
            full_url = response.urljoin(link)
            # Skip "videos" and "photos" categories
            if "videos" not in full_url and "photos" not in full_url:
                yield scrapy.Request(url=full_url, callback=self.parse_category)

    def parse_category(self, response):
        # Extract all URLs from the category page
        articles = response.css("div.cartHolder.listView.track.timeAgo a::attr(href)").getall()

        # Filter out non-article URLs (e.g., categories, authors) and remove duplicates
        unique_articles = list(set([url for url in articles if url.endswith(".html")]))

        # Process each unique article URL
        for article in unique_articles[:5]:
            full_url = response.urljoin(article)
            # Skip "videos" and "photos" categories
            if "videos" not in full_url and "photos" not in full_url:
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

        # Skip articles in the "videos" and "photos" categories
        if category_name in ["videos", "photos"]:
            return

        # Extract detailed article information
        item = NewsScraperItem()
        item['title'] = response.css("h1.hdg1::text").get()  # Adjust selector for article title
        item['url'] = response.url
        item['description'] = response.css("h2.sortDec::text").get()  # Meta description
        item['content'] = " ".join(response.css("div.detail p::text").getall())  # Full article content
        item['image_url'] = response.css("span picture img::attr(src)").get()  # Featured image
        item['source'] = "Hindustan Times"  # Static source field

        # Extract published date and time
        item['published_at'] = response.css("div.dateTime.secTime.storyPage::text").get()  # Adjust selector for published date
        item['is_kid_friendly'] = False  # Default value
        item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        item['categories'] = [category_name]  # Add the category name extracted from the URL
        if item["content"] and item["title"]:
            # Only yield the item if content and title are present
            yield item
