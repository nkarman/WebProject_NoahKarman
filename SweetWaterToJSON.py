import requests
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import urllib

# get today's date
today = str(datetime.datetime.now().date())

# initialize array of responses to be appended to JSON
response = []
browser = webdriver.Chrome()

# retrieve how many pages of items there are
sweetWaterURL = 'https://tradingpost.sweetwater.com/call/TP_Date/desc/1'
pageSW = browser.get(sweetWaterURL)
soupSW = BeautifulSoup(browser.page_source, 'lxml')
numOfPages = soupSW.find('div', class_='pagecount')
firstPage, lastPage = str(numOfPages.contents[0]).split("of ")
lastPage, trash = lastPage.split("<")
lastPage =int(lastPage)
# true if there is another page of items to be parsed, false when currPage is lastPage
nextPage = True

for pageNum in range(1,lastPage+2):
    pageSW = browser.get(sweetWaterURL)
    soupSW = BeautifulSoup(browser.page_source, 'lxml')
    sweetWaterURL = 'https://tradingpost.sweetwater.com/call/TP_Date/desc/' + str(pageNum)

    # for loop for parsing
    for position in soupSW.find_all('tr', bgcolor='ffffff'):
        # get positions for item, date posted, and product price
        itemPosition = position.contents[1]
        datePosition = position.contents[3]
        pricePosition = position.contents[5]

        # list to hold split string elements from each item
        itemElements = []
        itemHTML = itemPosition.contents[0]
        # get location from position
        location = itemPosition.contents[4]

        itemHTML = str(itemHTML)
        # split item into array of strings containing info on item
        itemElements = itemHTML.split("-")

        # Try-catch for index out of bounds - this occurs if itemHTML is not actually an item to parse
        try:
            # get location
            location = str(location.contents[0])
            # if no location is given, description mistakenly appears here
            if location.__len__() > 20:
                location = "n/a"

            # item condition is always first string in itemElements
            condition = itemElements[1]
            if condition == 'likenew':
                condition = 'like new'

            # item Make is always second string in itemElements
            make = itemElements[2]


            # item Model is made up of several strings in itemElements, but is delimited by "
            trash, productLinkEl = str(itemHTML).split("href=\"/")
            productLink, trash = productLinkEl.split("\"><img")
            productLink = urllib.parse.quote_plus(productLink)
            productLink = 'https://tradingpost.sweetwater.com/' + productLink

            model = ""

            # append all subStrings making up the item model into a singular string
            if "\"" not in model:
                for x in range(3,itemElements.__len__()):
                    model += itemElements[x] + " "
                title = make + " " + model
                titleList = title.split("\"")
                title = titleList[0]

            price = str(pricePosition.contents[0].contents[0])

            # get info from each product's individual page
            productPage = browser.get(productLink)
            productSoup = BeautifulSoup(browser.page_source, 'lxml')

            catPosition = productSoup.find('td', class_='info')
            category = catPosition.contents[1].contents[14].string
            productID = catPosition.contents[1].contents[23].string

            descPosition = productSoup.find('div', class_='desc')
            description = descPosition.contents[2].string



            print(condition, title, description, location, price, category,)


        except (IndexError, AttributeError, ValueError):
            print('Exception Caught')

        # append data to JSON
        if title != "n/a":
            response.append({'productTitle': title,
                        'productCondition': condition,
                             'productPrice': price,
                         'productLocation': location,
                             'productLink': productLink,
                             'productCategory': category,
                             'productID': productID,
                             'productDescription': description})

    # check if current page is the last available
    if (requests.get(sweetWaterURL) is None):
        nextPage = False
        browser.quit()

# shutdown chromeDriver
browser.quit()

# write JSON file
postingsFile = '/Users/NoahKArman/Documents/CSC 3130/WebProject_NoahKarman/JSON/' + today + '.SWSed.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=True, indent=2)

outfile.close()
