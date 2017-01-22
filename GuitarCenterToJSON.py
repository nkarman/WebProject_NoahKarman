import requests
import datetime
from bs4 import BeautifulSoup
import json
import csv

today = str(datetime.datetime.now().date())

# Create a list of dictionaries for JSON Object
response = []

# Scrape GuitarCenter with requests
gcUsedURL = 'http://www.guitarcenter.com/Used/'
pageGCUsed = requests.get(gcUsedURL)

# Prepare for parsing APNewsBriefs with BeautifulSoup
soupGCUsed = BeautifulSoup(pageGCUsed.content, 'lxml')

# Parse APNewsBriefs url
# 'position' marks the beginning of each news brief in the html
# All other data is found in its relationship to 'position'
for position in soupGCUsed.find_all('div', class_='productDetails'):
    #title
    titlePosition = position.find('div', class_='productTitle')
    title = titlePosition.find('a').string

    #link
    link = 'https://guitarcenter.com' + titlePosition.contents[1].contents[1].attrs['href']

    #condition
    conditionPosition = position.find('div', class_='productCondition')
    condition = conditionPosition.contents[0]

    #price
    pricePosition = position.find('span', class_='productPrice')
    price = (pricePosition.contents[2] + '.' + pricePosition.contents[3].contents[0])[:-3]

    #location
    locationPosition = position.find('div', class_='storeName')
    location = locationPosition.contents[3].string

    # attempt to open productPage URL. it looks like guitarCenter is blocking me out :(
    #productPage = requests.get(link)
    #soupProductPage = BeautifulSoup(productPage.content, 'lxml')

    #categoryPosition = soupProductPage.find("a", class_='category')
    #category = categoryPosition.contents[0]

    # Make changes to response for GCUsed
    response.append({'productTitle': title,
                     'productCondition': condition,
                     'productPrice': price,
                     'productLocation': location,
                     'productLink': link})

# Write response to JSON file
postingsFile = today + '.GCUSed.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=True, indent=2)

outfile.close()