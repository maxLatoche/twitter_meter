from datetime import datetime, timedelta
import requests
import pandas as pd
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()
base_url = u'https://twitter.com/search?'
query = u'f=tweets&vertical=default&q=%24BTC'
url = base_url+query
browser.get(url)
body = browser.find_element_by_tag_name('body')
tweets = body.find_elements_by_xpath('//li[@data-item-type="tweet"]')
now = datetime.now()
then = datetime.now() - timedelta(minutes=240)


def get_tweets(new_elements):
    for tweet in new_elements:
        # get tweet times
        time_stamp = tweet.find_element_by_class_name('tweet-timestamp')
        time_string = time_stamp.get_attribute('title')
        # convert time string to datetime object
        try:
            datetime_object = datetime.strptime(
                time_string, '%I:%M %p - %d %b %Y')
        except ValueError:
            continue
        # if time is greater than now-1 hour add ...
        # down_page command and add to count
        if datetime_object > then:
            continue
        else:
            return False
    return True


def tweet_counter():
    tweets = body.find_elements_by_xpath('//li[@data-item-type="tweet"]')
    browser.quit()
    return len(tweets)


def get_btc_price():
    url = u'https://coinmarketcap.com/'
    source_code = requests.get(url)
    source_code = source_code.text
    soup = BeautifulSoup(source_code, 'html.parser')
    btc_row = soup.find(id='id-bitcoin')
    btc_dict = {}
    btc_dict['market_cap'] = btc_row.contents[5].text.replace('\n', '').strip()
    btc_dict['price'] = btc_row.contents[7].text.replace('\n', '').strip()
    btc_dict['circulating_supply'] = btc_row.contents[9].text.replace('\n', '').replace('BTC', '').strip()
    btc_dict['volume'] = btc_row.contents[11].text.replace('\n', '').strip()
    btc_dict['change'] = btc_row.contents[13].text.replace('\n', '').strip()
    return btc_dict


while True:
    if get_tweets(tweets):
        body.send_keys(Keys.END)
    else:
        break
    time.sleep(2)
    body = browser.find_element_by_tag_name('body')
    tweets = body.find_elements_by_xpath('//li[@data-item-type="tweet"]')

btc_count = tweet_counter()

btc_data = get_btc_price()

btc_data['twitter_mentions'] = btc_count


def write_to_file():
    csv_file = Path('./btc_data.csv')
    if not csv_file.exists():
        df = pd.DataFrame(btc_data, index=[now, ])
        print(df)
        df.to_csv('btc_data.csv')
    else:
        csv_file = pd.read_csv('./btc_data.csv', 'a')
        df = pd.DataFrame(btc_data, index=[now, ])
        print(df)
        df.to_csv('./btc_data.csv', mode='a')


write_to_file()
