
from src.crawler import Crawler
from src.config import Config
import time
from src.progress import Progress


def main(url, config):

    crawler = Crawler(Config())
    crawler.scrape(url, 'bgpstream_results_'+ str(time.time())[:10] +'.csv')

def run_scraping():
    try:
        progress = Progress()
        progress.init()
        progress.save_process_progress(False,False)
        #browser = setup_browser()
        config = Config()
        url = config.initial_page
        main(url, config)

    except Exception as e:
        print(e)

if __name__ == '__main__':

    config = Config()
    main(config.host, config)
