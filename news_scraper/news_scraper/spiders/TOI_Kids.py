import scrapy
from datetime import datetime
from news_scraper.items import NewsScraperItem
import logging
import re


class TimeOfIndiaSpider(scrapy.Spider):
    name = "TOI_Kids"
    allowed_domains = ["toistudent.timesofindia.indiatimes.com"]
    start_urls = ["https://toistudent.timesofindia.indiatimes.com/news/top-news/"]
    page_count = 0  # Add page counter
    
    def parse(self, response):
        # Extract article links with better selectors
        article_links = response.css("div.usrcont a[href^='https://']::attr(href), div.most_text a[href^='https://']::attr(href)").getall()
        
        # Filter out any javascript: links
        valid_links = [link for link in article_links if link.startswith('https://')]
        
        for link in valid_links:
            try:
                yield response.follow(link, callback=self.parse_article)
            except Exception as e:
                logging.error(f"Error following link {link}: {str(e)}")
        
        # Modified pagination handling
        if self.page_count < 3:  # Only proceed if less than 3 pages
            next_page = response.css('a.next[href^="https://"]::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        try:
            item = NewsScraperItem()
            
            # Title extraction with better error handling
            title = response.css("div.maindiv h1::text, h1.article-title::text").get()
            item["title"] = title.strip() if title else ""
            
            # Image URL with multiple selector attempts
            item["image_url"] = (
                response.css("div.storyImg img::attr(src), "
                           "div.article-img img::attr(src), "
                           "div.storyImg img::attr(data-src)").get()
            )
            
            # Extract content (handling nested <span> elements)
            content_parts = response.css("div.storydetails p *::text").getall()
            cleaned_content = []

            for part in content_parts:
                part = part.strip()

                # Remove promotional lines and long dashed lines
                if not re.search(r"(LIKE this story and share with others too|Students, LIKE this story)", part, re.IGNORECASE) and \
                not re.match(r"^-{5,}$", part):  # Removes lines with 5 or more dashes

                    cleaned_content.append(part)

            item["content"] = " ".join(cleaned_content)
            
            # **Extract and clean date (Only Date, No Time)**
            date_text = response.css("li.date::text").get("")
            date_text = date_text.replace("Publish Date:", "").strip()

            try:
                # Convert to date format (ignoring time)
                parsed_date = datetime.strptime(date_text, "%b %d %Y %I:%M%p").date()
                item["published_at"] = parsed_date.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
            except ValueError:
                item["published_at"] = None  # Set to None if parsing fails

            
            # Categories extraction
            categories = response.css("div.article-tags span::text, div.categories a::text").getall()
            item["categories"] = categories if categories else ["General"]
            
            # Static and required fields
            item["source"] = "Times of India Student"
            item["url"] = response.url
            item["is_kid_friendly"] = True
            item["created_at"] = datetime.now()
            
            # Only yield item if we have at least title or content
            if item["title"] or item["content"]:
                yield item
            
        except Exception as e:
            logging.error(f"Error parsing article {response.url}: {str(e)}")