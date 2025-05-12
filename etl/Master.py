import os
import asyncio
import logging
from pathlib import Path
import sys
from datetime import datetime
import traceback

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from etl.Extract import extract_data
from etl.Transform import transform_data
from etl.Load import load_data

def setup_logging():
    """Configure detailed logging"""
    log_file = f"etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )

async def main():
    """Enhanced ETL pipeline with better error handling"""
    setup_logging()
    logger = logging.getLogger("ETL-Pipeline")
    
    try:
        logger.info("🚀 Starting ETL pipeline")
        
        # Extract phase with timeout and validation
        async with asyncio.timeout(3600):
            raw_data = await extract_data()
            if not raw_data:
                raise ValueError("Extraction phase returned no data")
            logger.info(f"Extracted {len(raw_data)} articles")

        # Transform phase with validation and error count tracking
        transformed = transform_data(raw_data)
        error_count = sum(1 for article in transformed if article.get('time_window') is None)
        if error_count:
            logger.warning(f"Transform phase had {error_count} date parsing errors")
        
        if not transformed:
            raise ValueError("Transform phase returned no data")
        logger.info(f"Transformed {len(transformed)} articles")
            
        # Load phase with timeout and connection validation
        async with asyncio.timeout(1800):
            try:
                success = await load_data(transformed)
                if not success:
                    raise ValueError("Load phase failed")
            except ConnectionError as ce:
                logger.error(f"Database connection failed: {str(ce)}")
                raise
        
        logger.info("🏁 ETL pipeline completed successfully")
        
    except asyncio.TimeoutError:
        logger.error("ETL pipeline timed out")
    except ValueError as ve:
        logger.error(f"ETL pipeline validation error: {str(ve)}")
    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}\n{traceback.format_exc()}")
    finally:
        logger.info("ETL pipeline shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.warning("ETL pipeline interrupted by user")