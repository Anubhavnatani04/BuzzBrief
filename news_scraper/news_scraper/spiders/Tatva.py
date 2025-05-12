import scrapy
from news_scraper.news_scraper.items import NewsScraperItem
from datetime import datetime
from urllib.parse import urlparse


class TatvaSpider(scrapy.Spider):
    name = "Tatva"
    allowed_domains = ["thetatva.in"]
    start_urls = ["https://thetatva.in"]

    def parse(self, response):
        # Extract category links from the homepage
        category_links = response.css("a.navbar_name.open_tab::attr(href)").getall()  # Adjust selector as needed

        for link in category_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(url=full_url, callback=self.parse_category)

    def parse_category(self, response):
        # Extract article links from the category page
        articles = response.css("a.gh-archive-page-post-title-link::attr(href)").getall()  # Adjust selector as needed

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
        
        # Extract the category name after the domain
        category_name = path_segments[0] if len(path_segments) > 0 else "Unknown"


        # Extract detailed article information
        item = NewsScraperItem()
        item['title'] = response.css("h1.gh-post-page__title::text").get()  # Adjust selector for article title
        item['url'] = response.url
        item['description'] = response.css("h2.gh-post-page__excerpt::text").get()  # Meta description
        item['content'] = " ".join(response.css("div.post-content p span::text, p.MsoNormal::text").getall()).strip()  # Full article content
         # Skip the article if content is empty
        if not item['content']:
            self.logger.info(f"Skipping article due to empty content: {response.url}")
            return

        item['image_url'] = response.css("img.gh-post-page__image::attr(src)").get()  # Featured image
        item['source'] = "The Tatva"  # Static source field

        # Extract published date and time
        item['published_at'] = response.css("time.gh-post-info__date::text").get().strip()  # Extract raw text

        item['is_kid_friendly'] = False  # Default value
        item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        item['categories'] = [category_name]  # Add the category name extracted from the URL
        
        if item["title"] and item["content"]:
            yield item