from pathlib import Path
import pandas as pd
import json
import requests
import numpy as np
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src.progress import Progress


class Crawler:
    def __init__(self,config):
        self.config = config

    def crawl_all_pages_to_end(self,initial_url,file_to_save_results):
        try:

            # Create dataframe to hold the data
            dataframe_file = Path(file_to_save_results)
            if(not dataframe_file.exists()):
                dataframe = pd.DataFrame()
            else:
                dataframe = pd.read_csv(file_to_save_results)

            # Get html for the given website
            session = requests.Session()
            session.headers.update({
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
            })
            response = session.get(self.config.initial_page)

            # Get the list of elements
            html_soup = BeautifulSoup(response.text, 'html.parser')
            list_items = html_soup.select('#all_events tbody tr')

            progress = Progress()


            total_number_items = len(list_items)
            progress.save_total_number_items(total_number_items)
            progress.save_process_progress(False,False)

            list_of_list = np.array_split(list_items,500)

            for list in list_of_list:
                for item in list:
                    item_dict = self.convert_to_dictionary(item)
                    item_serie = pd.Series(item_dict,index= item_dict.keys())

                    dataframe = dataframe.append(item_serie, ignore_index=True)
                    progress.save_number_items_scraped_so_far(dataframe.shape[0])
                    progress.add_item_scraped(item_dict)
                    progress.save_process_progress(False,False)

                dataframe.to_csv(file_to_save_results)

            progress.save_process_progress(True,False)
            return True
        except Exception as e:
            print(str(e))
            progress.save_process_progress(True,True)
            return False

    def scrape(self, initial_url, file_to_save_results):
        print("Start crawling...")

        got_to_end = self.crawl_all_pages_to_end(initial_url,file_to_save_results)
        if(got_to_end):
            print('Scraping finished successfully')
        else:
            print("Error during scraping")

        print("Finish crawling...")

    def convert_to_dictionary(self, web_element_in_numpy_array):
        item_dictionary = {}
        element_list = web_element_in_numpy_array.tolist()
        for element in element_list:
            if not isinstance(element, ''.__class__):
                if('event_type' in element.get('class')):
                    item_dictionary["Event Type"] = element.text
                    continue
                if('asn' in element.get('class')):
                    item_dictionary["ASN"] = element.text
                    continue
                if('startime' in element.get('class')):
                    item_dictionary["Start Time"] = element.text
                    continue
                if('endtime' in element.get('class')):
                    item_dictionary["End Time"] =element.text
                    continue
                if('moredetails' in element.get('class')):
                    item_dictionary["Event Url"] = urljoin(self.config.host,element.select('a')[0].get('href'))
                    continue

        return item_dictionary