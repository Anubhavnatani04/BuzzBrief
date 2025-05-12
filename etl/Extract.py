from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from collections import defaultdict
from typing import List, Dict, Any
import logging
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from news_scraper.news_scraper.spiders import (
    ChildrenspostSpider,
    EconomicTimesSpider,
    NewsahootSpider,
    OutlookSpider,
    RobinageSpider,
    TimeForKidsSpider,
    TOI_kidsSpider, 
    HindustantimesSpider,
    IndianexpressSpider,
    IndiatodaySpider,
    ThestatesmanSpider,
    RepublicworldSpider,
    ThehinduSpider,
    TimesofindiaSpider,
    TatvaSpider
)

class ExtractionManager:
    def __init__(self):
        self.settings = get_project_settings()
        self.runner = CrawlerRunner(self.settings)
        self.results: List[Dict[str, Any]] = []
        self.spider_counts = defaultdict(int)  # Track counts per spider

    def _handle_item(self, item, response, spider):
        """Callback method to collect items"""
        self.results.append(dict(item))
        self.spider_counts[spider.name] += 1  # Increment count for this spider
        # Free memory for item and response
        del item
        del response
        import gc
        gc.collect()

    @defer.inlineCallbacks
    def crawl_with_runner(self):
        try:
            spiders = [
                ChildrenspostSpider,
                EconomicTimesSpider,
                NewsahootSpider,
                OutlookSpider,
                RobinageSpider,
                TimeForKidsSpider,
                TOI_kidsSpider, 
                HindustantimesSpider,
                IndianexpressSpider,
                IndiatodaySpider,
                RepublicworldSpider,
                ThehinduSpider,
                ThestatesmanSpider,
                TimesofindiaSpider,
                TatvaSpider
            ]
            
            # Connect the signal for item scraped
            dispatcher.connect(self._handle_item, signal=signals.item_scraped)
            
            # Use a list to hold deferreds for each spider crawl
            deferreds = []
            for spider_class in spiders:
                deferred = self.runner.crawl(spider_class)
                deferreds.append(deferred)
            
            # Wait for all spiders to complete
            yield defer.DeferredList(deferreds)
            
            # Log results for each spider
            total_articles = sum(self.spider_counts.values())
            logging.info("Spider completion summary:")
            for spider_name, count in self.spider_counts.items():
                percentage = (count / total_articles * 100) if total_articles > 0 else 0
                logging.info(f"  {spider_name}: {count} articles ({percentage:.1f}%)")
            
            # Disconnect the signal after all crawlers finish
            dispatcher.disconnect(self._handle_item, signal=signals.item_scraped)
            
            reactor.stop()
        except Exception as e:
            logging.error(f"Spider execution failed: {str(e)}")
            reactor.stop()

async def extract_data() -> List[Dict[str, Any]]:
    """Execute all spiders and collect results with proper error handling"""
    logging.info("🕷️ Starting article extraction")
    
    try:
        manager = ExtractionManager()
        # Schedule the crawl to run when the reactor starts
        reactor.callWhenRunning(manager.crawl_with_runner)
        reactor.run(installSignalHandlers=False)
        
        if not manager.results:
            logging.warning("No articles extracted from any source")
            return []
            
        logging.info(f"✅ Successfully extracted {len(manager.results)} articles")
        return manager.results
        
    except Exception as e:
        logging.error(f"Extraction failed: {str(e)}")
        return []
    finally:
        if reactor.running:
            reactor.stop()
        # Free memory for results
        del manager.results
        del manager
        import gc
        gc.collect()