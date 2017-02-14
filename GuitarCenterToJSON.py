import requests
import datetime
from bs4 import BeautifulSoup
import json
from selenium import webdriver

today = str(datetime.datetime.now().date())

# Create a list of dictionaries for JSON Object
response = []

# Create a list of urls, and perform parsing for every URL
URLs = []

# Scrape GuitarCenter first used gear page for total number of products for sale
gcUsedURL = 'http://www.guitarcenter.com/Used/'
URLs.append(gcUsedURL)

pageGCUsed = requests.get(gcUsedURL)
soupGCUsed = BeautifulSoup(pageGCUsed.content, 'lxml')
# currPageNum will always have initial value of 100, this is the required value for the second page
currPageNum = 100
totalProducts = soupGCUsed.find('var', class_='searchTotalResults').contents[0]
totalProducts = int(totalProducts)
# last page of data
endPageNum = totalProducts-100

# populates list of urls with every url for every page containing used gear
while currPageNum < endPageNum:
    currPageNum += 100
    nextURL = 'http://www.guitarcenter.com/Used/#pageName=used-page&N=1076&Nao=' + str(currPageNum) + '&recsPerPage=100&v=g&postalCode=37212&radius=100&profileCountryCode=US&profileCurrencyCode=USD'
    URLs.append(nextURL)
# parse data for every URL in list
for url in URLs:
    pageGCUsed = requests.get(url)
    soupGCUsed = BeautifulSoup(pageGCUsed.content, 'lxml')
    print(url)
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

        #nextLink
        nextLinkPosition = position.find('div', class_='searchPagination')

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
postingsFile = '/Users/NoahKArman/Documents/CSC 3130/WebProject_NoahKarman/JSON/' + today + '.GCUSed.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=True, indent=2)

outfile.close()