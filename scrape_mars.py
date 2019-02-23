from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import datetime as dt
import pandas as pd
from pprint import pprint
import requests

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_data():
    # empty dictionary which will hold all scraped data, allows for mongoDB storage
    mars_dict = dict()
    
    # MARS NEWS
    # set up splinter and beautiful soup for the news page
    news_url = 'https://mars.nasa.gov/news'
    browser = init_browser()
    browser.visit(news_url)
    html = browser.html
    time.sleep(1)
    soup_news = bs(html, "html.parser")

    # get article title and paragraph from the first headline
    slide = soup_news.select_one('ul.item_list li.slide')
    titles = slide.find("div", class_="content_title").get_text()
    news_p = slide.find("div", class_="article_teaser_body").get_text()

    # append title and paragraph to mars_dict
    mars_dict['News Title'] = titles
    mars_dict['News Paragraph'] = news_p

    # MARS FEATURE IMAGE
    # navigate to new page to get image url
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # click on full image using splinter
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)

    # click more info button and then get the url for largesize image, combine with base url
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    html = browser.html
    img_soup = bs(html, 'html.parser')
    
    # find the relative image url
    img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    feature_url = 'https://www.jpl.nasa.gov' + img_url_rel

    # append feature_url to mars_dict
    mars_dict['Mars Feature Image URL'] = feature_url

    # MARS WEATHER
    # navigate to mars weather twitter page and set up beautiful soup
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)
    html = browser.html
    time.sleep(1)
    soup_tweet = bs(html, 'html.parser')

    # scrape the twitter page, obtaining the weather information from the latest tweet
    weather_info = soup_tweet.find('p', class_= 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    print(weather_info)

    # append weather information to mars_dict
    mars_dict['Mars Weather Information'] = weather_info

    # MARS FACTS
    # navigate to mars facts page and initiate beautiful soup
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    html = browser.html
    time.sleep(1)
    soup_facts = bs(html, 'html.parser')

    # scrap the table using pandas
    tables = pd.read_html(facts_url)
    tables

    # convert the table into a dataframe and set field as the index
    df = tables[0]
    df.columns = ['Field', 'Value']
    df = df.set_index('Field')
    df

    # convert dataframe into an html, get rid of \n
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')

    # append mars facts table to mars_dict
    mars_dict['Mars Facts Table'] = html_table

    # Mars Hemisphere Pictures
    # navigate to url and set up splinter
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    html = browser.html
    time.sleep(1)

    # set up beautiful soup and set all class=item to variable hemis
    soup_hemi = bs(html, 'html.parser')
    hemis = soup_hemi.find_all('div', class_='item')

    # iterate throught each of the item classes

    hemi_dict = []

    for hemi in hemis:
    
        # extract title which is located in each of the h3 tags
        title = hemi.find('h3').text
    
        # find the reference link for the enlarged image
        target_url = hemi.find("a", "itemLink product-item")['href']
    
        # combine this link with the base url to make the enlarged image url
        click_url = 'https://astrogeology.usgs.gov' + target_url
    
        # visit the new url with the enlarged image and create a new instance of beautiful soup
        browser.visit(click_url)
        html = browser.html
        time.sleep(1)
        soup_click = bs(html, 'html.parser')
    
        # navigate to the source for the jpg of the enlarged image then combine this with the base url
        img = soup_click.find('img', class_='wide-image')['src']
        img_url = 'https://astrogeology.usgs.gov' + img

        # append titles in results to hemi_dict
        hemi_dict.append({'title': title, 'img_url':img_url})

        print(hemi_dict)

        # append hemi_dict to mars_dict
        mars_dict['Hemisphere URLs'] = hemi_dict

    # add current date and time to mars_dict
    current_dt = dt.datetime.utcnow()
    mars_dict['Date_Time'] = current_dt

    final_dict = {
        'News_Headline': mars_dict['News Title'],
        'News_Paragraph': mars_dict['News Paragraph'],
        'Feature_Image_URL': mars_dict['Mars Feature Image URL'],
        'Mars_Current_Weather': mars_dict['Mars Weather Information'],
        'Mars_Facts_Table': mars_dict['Mars Facts Table'],
        'Mars_Hemispheres': mars_dict['Hemisphere URLs'],
        'Date_Time': mars_dict['Date_Time']
    }

    browser.quit()
    return final_dict