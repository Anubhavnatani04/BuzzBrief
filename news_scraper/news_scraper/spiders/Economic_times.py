import scrapy
from datetime import datetime
from news_scraper.news_scraper.items import NewsScraperItem

class EconomicTimesSpider(scrapy.Spider):
    name = "Economic_times"
    allowed_domains = ["economictimes.indiatimes.com"]
    
    # Define base URL and categories we want to scrape
    base_url = "https://economictimes.indiatimes.com"
    categories = [
        "news/india",
        "news/international",
        "news/politics",
        "news/science",
        "environment",
        "tech",
        "industry"
    ]
    
    def start_requests(self):
        # Generate start URLs for each category
        for category in self.categories:
            url = f"{self.base_url}/{category}"
            yield scrapy.Request(url, callback=self.parse_category, meta={'category': category})

    def parse_category(self, response):
        category = response.meta['category']
        
        if category == 'news/international' or category == 'industry' or category == 'environment':
            # Special selectors for international news
            article_links = response.css('div.featured h2 a::attr(href), div.top-news a::attr(href)').getall()[:10]
        elif category == 'news/politics':
            # Special selectors for politics news
            article_links = response.css('section#bottomPL a::attr(href)').getall()[:10]
        elif category == 'tech':
            # Special selectors for tech news
            article_links = response.css('div.top-stories.flt.prel h2 a::attr(href), div.sideStories.flr h4 a::attr(href), div.top-below-stories.clr h4 a::attr(href)').getall()[:10]
        else:
            # Original selectors for other categories
            article_links = response.css('div.eachStory h3 a::attr(href)').getall()[:10]
        
        for link in article_links[:10]:
            # Make sure we have full URL
            if link.startswith('/'):
                link = self.base_url + link
            yield scrapy.Request(
                link, 
                callback=self.parse_article,
                meta={'category': category}
            )

    def parse_article(self, response):
        try:
            item = NewsScraperItem()
            
            # Extract basic article details
            item['title'] = response.css('h1.artTitle::text, h1.title::text').get(default="").strip()
            
            # Get the full article content, excluding promotional divs
            content_selector = 'div.artText'
            article_content = response.css(content_selector)
            
            # Remove all promotional and unwanted divs
            unwanted_selectors = [
                'div.crypto.onDemand',
                'div.growfast_widget',
                'div.custom_ad',
                'div[style*="font-size"]',  # CSS style blocks
                'div.sr_widget',
                'div.stock_pro',
                'div#sr_widget',
                'div[data-ga-onclick]'  # Promotional links
            ]
            
            for selector in unwanted_selectors:
                article_content.css(selector).drop()
            
            # Extract text with a more comprehensive selector
            content_parts = article_content.css('p::text, p *::text, div::text').getall()
            
            # Clean and filter content
            cleaned_parts = []
            for part in content_parts:
                part = part.strip()
                if part and not any(x in part.lower() for x in [
                    'you can now subscribe',
                    'whatsapp channel',
                    '#sr_widget',
                    '.ondemand',
                    'font-size',
                    'padding:',
                    'margin:',
                    '{',
                    '}'
                ]):
                    cleaned_parts.append(part)
            
            item['content'] = " ".join(cleaned_parts)
            
            # Get image URL if available
            item['image_url'] = response.css('figure.articleImg img::attr(src), figure.artImg img::attr(src)').get()
            
            # Updated timestamp handling
            date_timestamp = response.css('time.jsdtTime::attr(data-dt)').get()
            if date_timestamp:
                # Convert milliseconds to seconds for Unix timestamp
                item['published_at'] = int(date_timestamp) / 1000
            else:
                # Default to current timestamp if not found
                item['published_at'] = datetime.now().timestamp()

            # Static fields
            item['source'] = "Economic Times"
            item['url'] = response.url
            item['is_kid_friendly'] = False
            item['created_at'] = datetime.now().timestamp()
            
            # Set categories based on URL path
            category = response.meta.get('category', 'news')
            item['categories'] = [category.split('/')[-1].capitalize()]
            
            # Get description (first few sentences of content)
            if item['content']:
                first_sentence = item['content'].split('.')[0] + '.'
                item['description'] = first_sentence
            else:
                item['description'] = item['title']
            
            if item['title'] and item['content']:
                yield item 
                
        except Exception as e:
            self.logger.error(f"Error parsing article {response.url}: {str(e)}")

    def errback_httpbin(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}")
