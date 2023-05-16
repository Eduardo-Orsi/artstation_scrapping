import re
import time
import logging
import sqlite3 as db
from typing import Union
from datetime import datetime
import xml.etree.ElementTree as ET

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from user_agents import get_random_user_agent


DB_NAME = "artstation.db"


class ArtstationScrapper:

    def __init__(self):
        self.start_execution = datetime.now()
        logging.basicConfig(filename=f'logs/{self.start_execution.strftime("%d.%m.%Y-%H.%M.%S")} Artstation Scrapping.log',
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            datefmt='%d-%m-%y %H:%M:%S')
        
        self.__get_chrome_options()
        #self.db_conn = self.__get_db_connection()

    def scrapp_profiles(self) -> None:
        df = pd.read_csv("artists_profile_urls.csv")
        urls = df['profile_urls'].to_list()

        start_time = time.time()
        for i in range(10):
            username = urls[i].split('/')[-1]
            url = f'https://{username}.artstation.com/resume'
            self.driver.get(f"https://webcache.googleusercontent.com/search?q=cache:{url}")
            time.sleep(3)
            print(f'https://{username}.artstation.com/resume')
            try:
                name = self.driver.find_element(By.CLASS_NAME, 'about-name')
                print(name.text)
            except:
                continue

            try:
                position = self.driver.find_element(By.CLASS_NAME, 'about-position')
                print(position.text)
            except:
                continue

            try:    
                email = self.driver.find_element(By.CLASS_NAME, 'about-email')
                print(email.text)
            except:
                continue

            print('--------------------------------------')
            self.clean_webdriver_data()
            self.change_user_agent()
            time.sleep(1)
        
        end_time = time.time()
        print("Execution time:", end_time - start_time)

    def get_artists_profile_urls(self, artists_sitemap_urls: list[str]) -> list[str]:

        if not artists_sitemap_urls:
            logging.error("Artists Sitemap URLs not provided in get_artists_profile_urls()")
            return None

        artists_profile_urls = []
        for sitemap_url in artists_sitemap_urls:
            try:
                self.driver.get(sitemap_url)
                page_source = self.driver.page_source

                soup = BeautifulSoup(page_source, 'html.parser')
                xml_tag = soup.find(id="webkit-xml-viewer-source-xml")
                urlset_tag = xml_tag.contents[0]
                for url in urlset_tag.find_all("loc"):
                    print(url.text)
                    artists_profile_urls.append(url.text)
        
            except Exception as ex:
                logging.error(f"Cannot resolve this URL: {sitemap_url} | {ex}")

        data = {
            "profile_urls": artists_profile_urls,
            "scrapped": False
        }
        df = pd.DataFrame(data)
        df.to_csv("artists_profile_urls.csv", index=False)

        return artists_profile_urls

    def get_artists_sitemaps_urls(self) -> list[str]:
        try:
            base_sitemap_url = 'https://www.artstation.com/sitemap.xml'

            self.driver.get(base_sitemap_url)
            page = self.driver.page_source

            soup = BeautifulSoup(page, 'html.parser')
            xml_content = soup.find("sitemapindex").prettify()

            root = ET.fromstring(xml_content)
            ns = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            artists_sitemap_urls = []
            pattern = r"https://www.artstation.com/sitemap-artists-\d+\.xml"
            for sitemap in root.findall('sitemap:sitemap', ns):
                url = sitemap.find('sitemap:loc', ns).text
                url = url.replace('\n', '').strip()
                url = re.match(pattern, url)
                if url:
                    print(url)
                    artists_sitemap_urls.append(url.string)

            return artists_sitemap_urls

        except Exception as ex:
            logging.error(f'Problem to get the base sitemap XML | {ex}')

    def get_artists_urls(self) -> None:
        df = pd.read_csv('artists_sitemap_urls.csv')

    def __get_chrome_options(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--incognito')
        options.add_argument("--headless")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument(f"user-agent={get_random_user_agent()}")
        options.add_argument("--mute-audio")
        options.add_argument("--log-level=3")

        experimental_flags = ['same-site-by-default-cookies@2', 'cookies-without-same-site-must-be-secure@1']
        chrome_local_state_prefs = {'browser.enabled_labs_experiments': experimental_flags}
        options.add_experimental_option('localState', chrome_local_state_prefs)

        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')

        options.add_experimental_option('prefs', {'intl.accept_languages': 'pt,pt_BR'})

        options.add_experimental_option('prefs', {
            'credentials_enable_service': True,
            'profile': {
                'password_manager_enabled': True,
                'exit_type': 'Normal'
            }
        })

        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": get_random_user_agent()})
        driver.maximize_window()
        self.driver = driver

    def change_user_agent(self) -> None:
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": get_random_user_agent()})

    def clean_webdriver_data(self) -> None:
        self.driver.delete_all_cookies()
        self.driver.execute_script('window.localStorage.clear();')
        self.driver.execute_script('window.sessionStorage.clear();')

    def __get_db_connection(self, db_name: str) -> Union[db.Connection, None]:
        try:
            conn = db.connect(f"DB/{db_name}")
            return conn
        except Exception as ex:
            logging.error(f"Problem to connect to the SQLite3 DB | {ex}")
            return None
        
if __name__ == "__main__":
    scrapper = ArtstationScrapper()
    # artists_sitemap_urls = scrapper.get_artists_sitemaps_urls()
    # artists_profile_urls = scrapper.get_artists_profile_urls(artists_sitemap_urls)
    # print(artists_profile_urls)
    scrapper.scrapp_profiles()

