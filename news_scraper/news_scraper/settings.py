import os
os.environ['TLD_EXTRACT_CACHE_DIR'] = './tldextract_cache'

# Scrapy settings for news_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "news_scraper"

SPIDER_MODULES = ["news_scraper.spiders"]
NEWSPIDER_MODULE = "news_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.121 Safari/537.36'

# Update downloader middleware settings
DOWNLOADER_MIDDLEWARES = {
    "news_scraper.middlewares.RandomUserAgentMiddleware": 400,
    "scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware": 550,
    "news_scraper.middlewares.NewsScraperSpiderMiddleware": 543,
    "news_scraper.middlewares.NewsScraperDownloaderMiddleware": 544,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
    "scrapy.downloadermiddlewares.httperror.HttpErrorMiddleware": 555,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 590,
    "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": None,
}

PROXY_POOL_ENABLED = True

# Added default headers to mimic a real browser and reduce 403 errors
# In settings.py, update DEFAULT_REQUEST_HEADERS:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept-Charset": "utf-8",
    "Content-Type": "text/html; charset=utf-8",
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.5  # Delay between requests (in seconds)
RANDOMIZE_DOWNLOAD_DELAY = True
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 3
AUTOTHROTTLE_MAX_DELAY = 30
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

ITEM_PIPELINES = {
    "news_scraper.pipelines.NewsScraperPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_LEVEL = 'CRITICAL'  # Logging 
HTTPERROR_ALLOWED_CODES = [403, 404, 429]  # added line to allow processing of 403 and 404 responses

# Add retry settings
RETRY_ENABLED = True
RETRY_TIMES = 1
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

# Add encoding settings
FEED_EXPORT_ENCODING = 'utf-8'
FEED_EXPORT_INDENT = 2

# Add response encoding settings
RESPONSE_ENCODING = 'utf-8'

# Force response encoding if needed
RESPONSE_FORCE_ENCODING = 'utf-8'

# Increase download timeout
# settings.py
CLOSESPIDER_TIMEOUT = 60  # Disable auto-timeout
CLOSESPIDER_ITEMCOUNT = 0  # Disable item count limit
DOWNLOAD_TIMEOUT = 10  # Increase timeout to 10s

RANDOM_DELAY = True

# Remove incorrect DOWNLOAD_HANDLERS setting and replace with correct one
DOWNLOAD_HANDLERS = {
    "http": "scrapy.core.downloader.handlers.http11.HTTP11DownloadHandler",
    "https": "scrapy.core.downloader.handlers.http11.HTTP11DownloadHandler", 
}

FEEDS = {
    'output.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'indent': 4,
    },
}

# Add these settings for better reliability
REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 5

# Add DNS cache for better performance
DNS_TIMEOUT = 10
DNSCACHE_ENABLED = True
DNSCACHE_SIZE = 10000

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"