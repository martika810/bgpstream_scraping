import threading
from src.main_bgpstream_scraper import run_scraping

class CrawlingThreading:
    def __init__(self,url):
        self.url = url
        thread = threading.Thread(target=self.run,args=())
        thread.daemon = True
        thread.start()

    def run(self):
        print('Thread to crawl freida has started')
        run_scraping()
