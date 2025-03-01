import scrapy
from datetime import datetime
from news_scraper.items import NewsScraperItem

class OutlookSpider(scrapy.Spider):
    name = "Outlook"
    allowed_domains = ["www.outlookindia.com"]
    start_urls = ["https://www.outlookindia.com"]

    def parse(self, response):
        links = response.css("div.article-heading-two a::attr(href)").getall()
        links.extend(response.css("div.article-heading-one a::attr(href)").getall())
        for link in links:
            yield response.follow(link, callback=self.parse_article)
    
    def parse_article(self, response):
        item = NewsScraperItem()
        # Extract title from h1 (update selector if needed)
        item["title"] = response.css("h1.story-title::text").get(default="").strip()
        # Extract and clean content
        content = " ".join(response.css("div.sb-article *::text").getall())
        # Remove ad-related content
        content = self.clean_content(content)
        item["content"] = content
        # Retrieve image URL, if present
        item["image_url"] = response.css("div.main-img-div img::attr(src)").get()
        # Extract published date from an assumed element; adjust selector as needed
        datetime_attr = response.css("div.story-dec-time time::attr(datetime)").get(default="")
        item["published_at"] = datetime_attr.split("T")[0] if "T" in datetime_attr else ""
        # Set static/required fields
        item["source"] = "Outlook India"
        item["url"] = response.url
        item["is_kid_friendly"] = False
        item["created_at"] = datetime.now()
        # Extract categories (if available)
        item["categories"] = response.css("p.story-slug *::text").getall()
        item["description"] = response.css("p.subcap-story::text").get()
        # Ensure title and content are not empty
        if item["title"] and item["content"]:
            yield item
    
    def clean_content(self, content):
        """Clean the content by removing ads and other noise."""
        # Remove ad-related JavaScript
        import re
        patterns = [
            r'var newSlot.*?</div></div>',  # Remove ad slots
            r'window\._taboola.*?}\);',      # Remove Taboola ads
            r'if\(isMobile\(\)\).*?}\n',     # Remove mobile-specific ads
            r'\s+',                          # Normalize whitespace
        ]
        
        cleaned = content
        for pattern in patterns:
            cleaned = re.sub(pattern, ' ', cleaned, flags=re.DOTALL)
            
        # Clean up extra whitespace
        cleaned = ' '.join(cleaned.split())
        
        return cleaned.strip()
