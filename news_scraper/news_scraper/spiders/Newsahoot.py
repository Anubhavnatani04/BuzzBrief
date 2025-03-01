import scrapy
from datetime import datetime
from news_scraper.items import NewsScraperItem
import json

class NewsahootSpider(scrapy.Spider):
    name = "Newsahoot"
    allowed_domains = ["newsahoot.com", "api.newsahoot.com"]
    start_urls = ["https://www.newsahoot.com/articles"]
    page_count = 1

    def parse(self, response):
        # Extract article links from the main news sections
        article_links = response.css("div.articleScreener_rapArticlesMainDiv__kbgW7 a::attr(href)").getall()
        for link in article_links:
            # Construct the full article URL
            full_article_url = response.urljoin(link)
            # Extract the slug from the link
            slug = link.split("/articles/")[-1]
            # Build the API endpoint
            api_url = f"https://api.newsahoot.com/api/news-article/{slug}?difficulty=INTERMEDIATE&state=FULL"
            yield scrapy.Request(api_url, callback=self.parse_api, meta={"article_url": full_article_url})

        # Handle pagination
        next_page = response.css("div.pagination_pg11JF__3s4Ax a::attr(href)").get()
        if next_page and self.page_count < 10:
            self.page_count += 1
            yield response.follow(next_page, callback=self.parse)


    def parse_api(self, response):
        data = json.loads(response.text)
        
        item = NewsScraperItem()
        item["id"] = 9  # Adjust as needed
        item["title"] = data.get("title", "")
        item["description"] = data.get("quick_revision", "")
        item["image_url"] = data.get("image", {}).get("formats", {}).get("thumbnail", {}).get("url", "")
        
        raw_body = data.get("intermediate_body", "")
        # Clean the HTML tags (choose one option)
        from w3lib.html import remove_tags
        clean_body = remove_tags(raw_body).strip()
        item["content"] = clean_body
        
        item["published_at"] = data.get("publishedAt", "")
        item["source"] = "Newsahoot"
        item["url"] = response.meta.get("article_url", "")
        item["is_kid_friendly"] = True
        item["created_at"] = datetime.now()
        item["categories"] = data.get("category", [])
        
        yield item
