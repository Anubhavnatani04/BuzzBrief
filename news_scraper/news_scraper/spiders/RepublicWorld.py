import scrapy
from news_scraper.news_scraper.items import NewsScraperItem
from datetime import datetime
from urllib.parse import urlparse

class RepublicworldSpider(scrapy.Spider):
    name = "RepublicWorld"
    allowed_domains = ["republicworld.com"]
    start_urls = ["https://republicworld.com"]

    def parse(self, response):
        # Extract category links from the homepage
        category_links = response.css("div.navbarlist.svelte-f2m4r1 a::attr(href)").getall()  # Adjust selector as needed

        for link in category_links:
            full_url = response.urljoin(link)
            # Skip "videos" and "photos" categories
            if "videos" not in full_url and "photos" not in full_url:
                yield scrapy.Request(url=full_url, callback=self.parse_category)

    def parse_category(self, response):
        # Extract article links from the category page
        articles = response.css("div.w-3\\/5.svelte-my3qq1 a::attr(href)").getall()  # Adjust selector as needed

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
        
        # Assume the category name is the first segment in the URL path
        category_name = path_segments[0] if len(path_segments) > 0 else "Unknown"

        # Skip articles in the "videos" and "photos" categories
        if category_name in ["videos", "video", "photo", "photos"]:
            return

        # Extract detailed article information
        item = NewsScraperItem()
        item['title'] = response.css("h1.svelte-7h8hl1::text").get()  # Adjust selector for article title
        item['url'] = response.url
        item['description'] = response.css("h2::text").get()  # Meta description
        item['content'] = " ".join(response.css("div#descwithads div p::text").getall()).strip()  # Cleaned content
        item['image_url'] = response.css("div.story-main-div-img.svelte-nt5009 img::attr(src)").get()  # Featured image
        item['source'] = "Republic World"  # Static source field

        # Extract published date and time
        published_at_raw = response.css("div.topStorycard.\\!w-full.svelte-7h8hl1 div p::text").get()  # Extract raw text
        if published_at_raw:
            # Remove "Updated" and clean the date and time
            published_at = published_at_raw.replace("Updated", "").strip()
            item['published_at'] = published_at
        item['is_kid_friendly'] = False  # Default value
        item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp
        item['categories'] = [category_name]  # Add the category name extracted from the URL
        if(item['title'] and item['content']):
            yield item