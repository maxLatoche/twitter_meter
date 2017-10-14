import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
base_url = u'https://twitter.com/search?q='
query = u'%40maxlatoche'
url = base_url+query

browser.get(url)
time.sleep(1)

body = browser.find_element_by_tag_name('body')

for _ in range(5):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)

r = requests.get(url+query)
soup = BeautifulSoup(r.text, 'html.parser')

tweets = browser.find_element_by_class_name('tweet-text')

# with open('twitter_meter_output.txt', 'w', encoding='utf-8') as text_file:
#     print(soup, file=text_file)
