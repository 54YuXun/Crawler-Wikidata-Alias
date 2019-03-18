import time
import argparse
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def xpath2href(driver, xpath):
    text = driver.find_element_by_xpath(xpath).get_attribute('href')
    return text


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest="k", action="store", help="Key in your Keyword", nargs=1)
    k = parser.parse_args().k
    return k

def wiki_crawler(Keyword, delay):
    list = []
    wikidata_url = "https://www.wikidata.org/wiki/Wikidata:Main_Page"
    driver = webdriver.Chrome()
    driver.get(wikidata_url)
    driver.find_element_by_id("searchInput").send_keys(Keyword)
    driver.find_element_by_xpath('//*[@id="searchButton"]').click()
    firstlink = '//*[@id="mw-content-text"]/div[4]/ul/li/div[1]/a'
    destination = xpath2href(driver, firstlink)
    Tag = destination.split('/')[-1]
    driver.get(destination)
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'wikibase-aliasesview-list-item')))
        # print ("Page is ready!")
        soup = BeautifulSoup(driver.page_source, "lxml")
        abc = soup.findAll("li", {"class": "wikibase-aliasesview-list-item"})
        for i in abc:
            try:
                list.append(i.text)
            except:
                return 0;
    except TimeoutException:
        print ("Loading took too much time!")
    return(list)

def main():
    Keyword = get_argument()[0]
    delay = 3
    dataset = wiki_crawler(Keyword, delay)
    print(dataset)

if __name__ == "__main__":
    main()
