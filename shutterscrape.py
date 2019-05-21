from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib import urlretrieve
import os
import Tkinter, Tkconstants, tkFileDialog
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def videoscrape():
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        for i in range(1, searchPage + 1):
            url = "https://www.shutterstock.com/video/search/" + searchTerm + "?page=" + str(i)
            driver.get(url)
            print("Page " + str(i))
            for j in range (0, 50):
                while True:
                    container = driver.find_elements_by_xpath("//div[@data-automation='VideoGrid_video_videoClipPreview_" + str(j) + "']")
                    if len(container) != 0:
                        break
                    if len(driver.find_elements_by_xpath("//div[@data-automation='VideoGrid_video_videoClipPreview_" + str(j + 1) + "']")) == 0 and i == searchPage:
                        driver.close()
                        return
                    time.sleep(10)
                    driver.get(url)
                container[0].click()
                while True:
                    wait = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH, "//video[@data-automation='VideoPlayer_video_video']")))
                    video_url = driver.current_url
                    data = driver.execute_script("return document.documentElement.outerHTML")
                    scraper = BeautifulSoup(data, "lxml")
                    video_container = scraper.find_all("video", {"data-automation":"VideoPlayer_video_video"})
                    if len(video_container) != 0:
                        break
                    time.sleep(10)
                    driver.get(video_url)
                video_array = video_container[0].find_all("source")
                video_src = video_array[1].get("src")
                name = video_src.rsplit("/", 1)[-1]
                try:
                    urlretrieve(video_src, os.path.join(scrape_directory, os.path.basename(video_src)))
                    print("Scraped " + name)
                except Exception as e:
                    print(e)
                driver.get(url)
    except Exception as e:
        print(e)

def imagescrape():
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        for i in range(1, searchPage + 1):
            url = "https://www.shutterstock.com/search?searchterm=" + searchTerm + "&sort=popular&image_type=all&search_source=base_landing_page&language=en&page=" + str(i)
            driver.get(url)
            data = driver.execute_script("return document.documentElement.outerHTML")
            print("Page " + str(i))
            scraper = BeautifulSoup(data, "lxml")
            img_container = scraper.find_all("img", {"class":"z_e_h"})
            for j in range(0, len(img_container)-1):
                img_src = img_container[j].get("src")
                name = img_src.rsplit("/", 1)[-1]
                try:
                    urlretrieve(img_src, os.path.join(scrape_directory, os.path.basename(img_src)))
                    print("Scraped " + name)
                except Exception as e:
                    print(e)
        driver.close()
    except Exception as e:
        print(e)

print("ShutterScrape v1.1")

#scrape_directory = "C:/Users/[username]/[path]"

while True:
    while True:
        print("Please select a directory to save your scraped files.")
        scrape_directory = tkFileDialog.askdirectory()
        if scrape_directory == None or scrape_directory == "":
            print("You must select a directory to save your scraped files.")
            continue
        break
    while True:
        searchMode = raw_input("Search mode ('v' for video or 'i' for image): ")
        if searchMode != "v" and searchMode != "i":
            print("You must select 'v' for video or 'i' for image.")
            continue
        break
    while True:
        searchCount = input("Number of search terms: ")
        if searchCount < 1:
            print("You must have at least one search term.")
            continue
        elif searchCount == 1:
            searchTerm = raw_input("Search term: ")
        else:
            searchTerm = raw_input("Search term 1: ")
            for i in range (1, searchCount):
                searchTermPart = raw_input("Search term " + str(i + 1) + ": ")
                if searchMode == "v":
                    searchTerm += "-" + searchTermPart
                if searchMode == "i":
                    searchTerm += "+" + searchTermPart
        break
    while True:
        searchPage = input("Number of pages to scrape: ")
        if searchPage < 1:
            print("You must have scrape at least one page.")
            continue
        break
    if searchMode == "v":
        videoscrape()
    if searchMode == "i":
        imagescrape()
    print("Scraping complete.")
    restartScrape = raw_input("Keep scraping? ('y' for yes or 'n' for no) ")
    if restartScrape == "n":
        print("Scraping ended.")
        break
