import asyncio
import logging
from Extract import extract_data
from Transform import transform_data
from Load import load_data

async def main():
    logging.info("Starting ETL pipeline")
    # Extract articles from web scrapers
    raw_articles = await extract_data()

    # Transform the raw articles (normalize, deduplicate fingerprints, etc.)
    transformed_articles = transform_data(raw_articles)

    # Load unique articles to the database
    await load_data(transformed_articles)

    logging.info("ETL pipeline completed")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())