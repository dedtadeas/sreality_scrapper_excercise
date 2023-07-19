import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import your spider class from your spider file
from spiders.flat_spider import FlatSpider

def run_spider():
    # Create a CrawlerProcess with project settings
    process = CrawlerProcess(get_project_settings())
    process.crawl(FlatSpider, int(os.getenv("SCRAPE_LIMIT", "5")))

    # Start the crawling process
    process.start()

if __name__ == "__main__":
   run_spider()
   print('run_spider()')