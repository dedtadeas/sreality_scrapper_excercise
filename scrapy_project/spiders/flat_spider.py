import scrapy, os
from items import FlatItem

class FlatSpider(scrapy.Spider):
    name = 'sreality'
    allowed_domains = ['sreality.cz']

    # Use custom_settings to set the number of concurrent requests and the pipeline to use
    custom_settings = {
        'CONCURRENT_REQUESTS': 32, 
        'ITEM_PIPELINES': {
            'pipelines.FlatsPipeline': 300,
        },
        'DOWNLOAD_DELAY' : 0.1,
    }

    # Create init function which takes scrape_limit as an argument
    def __init__(self, scrape_limit, *args, **kwargs):
        super(FlatSpider, self).__init__(*args, **kwargs)
        self.scrape_limit = int(scrape_limit)  

    def start_requests(self):
        # Scrape from 1 to 50 pages
        for page in range(1,  51):
            url = f'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=100&page={page}'
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
         jsonresponse = response.json()
         for item in jsonresponse["_embedded"]['estates']:
            yield scrapy.Request( 'https://www.sreality.cz/api' + item['_links']['self']['href'] ,
                          callback=self.parse_flat)

    def parse_flat(self, response): 
        self.scrape_limit -= 1   
        if self.scrape_limit < 0:
            # Stop the spider when scrape_limit runs out
            self.crawler.engine.close_spider(self, 'Reached scrape_limit')
            return

        
        jsonresponse = response.json()
        flat = FlatItem()
        flat['title'] = jsonresponse['name']['value']
        flat['image_url'] = jsonresponse['_embedded']['images'][0]['_links']['gallery']['href']
        yield flat
