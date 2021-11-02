#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 02:01:14 2021

@author: yinchunhsiao
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import requests
import os, sys
import docx

def write_doc(folder, url_current):
    """
    

    Parameters
    ----------
    folder : string
        path for storing word file
    url_current : string
        url for text parsing

    Returns
    -------
    soup : TYPE
        DESCRIPTION.

    """
    chrome_tmp = webdriver.Chrome('./chromedriver', chrome_options=options)
    chrome_tmp.get(url_current)
    res = requests.get(url_current)
    soup = bs(res.text, 'html.parser')
    # print(soup.prettify())
    chrome_tmp.close()
    # write word document
    mydoc = docx.Document()
    mydoc.add_paragraph(soup.text)
    date = soup.find_all('time', class_='bbc-529aew e4zesg50')[0].get('datetime')
    mydoc.save(os.path.join(folder, '%s_%s.docx'%(date, soup.title.text)))
    
    return soup
    
options = Options()
options.add_argument("--disable-notifications")
 
chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
chrome.get("https://www.google.com")
a = chrome.find_element_by_class_name('gLFyf.gsfi')
a.send_keys('新疆')
a.send_keys(Keys.ENTER)

#%% parse current url
url = chrome.current_url
response = requests.get(url)
soup = bs(response.text, 'html.parser')
print(soup.prettify())



#%% find title at google search engine
urls = []
q = soup.find_all('h3', class_='zBAuLc l97dzf')
for x in q:
    try:
        u = x.find_parent('a').get('href')
        urls.append(u)
    except:
        pass

# sys.exit(0)
#%% build folder to store news
folder = 'C:/Project/selenium/news/'
try:
    os.mkdir(folder)
except:
    pass

#%% parse news data and store to word file
u = []
# all_title = []    
all_url = []
for i, url in enumerate(urls):
    url_current = url[url.find('q=')+2: url.find('&sa')]
    u.append(url_current)
    if 'bbc' in url_current:
        # print(url_current)
        soup = write_doc(folder, url_current)
        all_url.append(url_current)
        # collect url of related context
        el = soup.find_all('li', class_='e57qer20 bbc-idn7y eom0ln51')
        current_url = []
        for j in range(len(el)):
            current_url.append(el[j].find('a', class_='bbc-1fxtbkn evnt13t0').get('href'))
        next_url = []

        while len(current_url) != 0 and len(all_url) < 50:
            for j in range(len(current_url)):
                current_url[j] = 'https://www.bbc.com' + current_url[j]
                if current_url[j] not in all_url:
                    all_url.append(current_url[j])
                    soup = write_doc(folder, current_url[j])
                    el = soup.find_all('li', class_='e57qer20 bbc-idn7y eom0ln51')
                    for k in range(len(el)):
                        next_url.append(el[k].find('a', class_='bbc-1fxtbkn evnt13t0').get('href'))
            current_url = next_url.copy()
            next_url = []