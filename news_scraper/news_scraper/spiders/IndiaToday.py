import scrapy
from news_scraper.news_scraper.items import NewsScraperItem
from datetime import datetime
from urllib.parse import urlparse

class IndiatodaySpider(scrapy.Spider):
    name = "IndiaToday"
    allowed_domains = ["indiatoday.in"]
    start_urls = ["https://indiatoday.in"]

    def parse(self, response):
        self.logger.info(f"Crawling page: {response.url}")
        # Extract category links from the homepage
        category_links = response.css("li.jsx-24eb2c73dea34577 a::attr(href)").getall()  # Adjust selector as needed

        # Define the allowed categories
        allowed_categories = ["india", "world", "sports", "technology", "business", "entertainment"]

        for link in category_links:
            full_url = response.urljoin(link)
            # Extract the category name from the URL
            category_name = urlparse(full_url).path.strip("/").split("/")[0]
            # Check if the category is in the allowed list
            if category_name in allowed_categories:
                yield scrapy.Request(url=full_url, callback=self.parse_category)

    def parse_category(self, response):
        # Extract articles from the category page
        articles = response.css("div.B1S3_content__wrap__9mSB6 h2 a::attr(href)").getall()  # Adjust selector as needed

        for article in articles[:10]:
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
        
        # Assume the category name is the first segment in the URL path
        category_name = path_segments[0] if len(path_segments) > 0 else "Unknown"

        # Extract detailed article information
        item = NewsScraperItem()
        item['title'] = response.css("div.jsx-ace90f4eca22afc7.lhs__section h1::text").get()  # Adjust selector for article title
        item['url'] = response.url
        item['description'] = response.css("div.jsx-ace90f4eca22afc7.lhs__section h2::text").get()  # Meta description
        item['content'] = " ".join(response.css("div.jsx-ace90f4eca22afc7.Story_description__fq_4S.description.paywall p::text").getall())  # Full article content
        item['image_url'] = response.css("div.Story_associate__image__bYOH_.topImage img::attr(src)").get()  # Featured image
        item['source'] = "India Today"  # Static source field

        # Extract published date and time
        published_at_list = response.css("span.jsx-ace90f4eca22afc7.strydate::text").getall()  # Extract all text
        published_at = "".join([text.strip() for text in published_at_list if text.strip() and "UPDATED" not in text])  # Clean up the text
        item['published_at'] = published_at  # Assign the cleaned-up date and time
        item['is_kid_friendly'] = False  # Default value
        item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        item['categories'] = [category_name]  # Add the category name extracted from the URL
        
        if item["title"] and item['content']:
            yield item
