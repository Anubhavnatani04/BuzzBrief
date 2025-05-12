from setuptools import setup, find_packages

setup(
    name="news-scraper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "scrapy>=2.11.0",
        "asyncio>=3.4.3",
        "asyncpg",
        "python-dotenv",
        "simhash",
        "datasketch",
        "nltk"
    ]
)