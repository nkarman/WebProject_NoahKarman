import requests
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import json

today = str(datetime.datetime.now().date())
# initialize array of responses to be appended to JSON
response = []
browser = webdriver.Chrome()

# page number to iterated through
pageNum = 1
reverbURL = 'https://reverb.com/marketplace?query=&condition=used&page=' + str(pageNum)
nextPage = True

while nextPage:
    pageReverb = browser.get(reverbURL)
    soupReverb = BeautifulSoup(browser.page_source, 'lxml')

    for position in browser.find_elements_by_class_name('product-card-description'):
        titlePosition = position.find_element_by_class_name('product-card-body-sized')
        soupTitle = BeautifulSoup(titlePosition, 'lxml')
        print(title)
        pricePosition = titlePosition.next
        conditionPosition = pricePosition.next


    pageNum += 1
    if (requests.get(reverbURL) is None):
        nextPage = False
        browser.quit()
