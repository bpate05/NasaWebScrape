from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_news():
    browser = init_browser()
    
    news_url = https://mars.nasa.gov/news
    browser.visit(news_url)
    html = browser.html
    time.sleep(3)
    soup_news = bs(html, "html.parser")
    
    titles = soup_news.find("div", id="content_title")
    news_title = titles.find_all("a").text.strip()
    news_p = soup_news.find("div", "article_teaser_body").text


def scrape_image():






def scrape_weather():




def scrape_facts():



def scrape_hemi():


    