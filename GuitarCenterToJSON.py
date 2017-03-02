import requests
import datetime
from bs4 import BeautifulSoup
import json
from selenium import webdriver

today = str(datetime.datetime.now().date())

# Create a list of dictionaries for JSON Object
response = []
browser = webdriver.Chrome('/Users/NoahKArman/Documents/CSC 3130/WebProject_NoahKarman/chromedriver')

# Create a list of urls, and perform parsing for every URL
URLs = []

# Scrape GuitarCenter first used gear page for total number of products for sale
gcUsedURL = 'http://www.guitarcenter.com/Used/'
URLs.append(gcUsedURL)

pageGCUsed = browser.get(gcUsedURL)
soupGCUsed = BeautifulSoup(browser.page_source, 'lxml')
# currPageNum will always have initial value of 100, this is the required value for the second page
currPageNum = 100
totalProducts = soupGCUsed.find('var', class_='searchTotalResults').contents[0]
totalProducts = int(totalProducts)
# last page of data
endPageNum = totalProducts-100

# populates list of urls with every url for every page containing used gear
# while currPageNum < endPageNum:
while currPageNum < 500:
    currPageNum += 100
    nextURL = 'http://www.guitarcenter.com/Used/#pageName=used-page&N=1076&Nao=' + str(currPageNum)
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

        # category
        category = ""
        lcTitle = title.lower()

        if "guitar" in lcTitle or "bass guitar" in lcTitle:
            category = "Guitar & Bass"
        if "mic" in lcTitle:
            category = "Microphones"
        # Amps & effects
        if "amp" in lcTitle or "pedal" in lcTitle or "footswitch" in lcTitle:
            category = "Amps & Effects"
        if "cymbal" in lcTitle or "snare" in lcTitle or "kick" in lcTitle or "drum" in lcTitle:
            category = "Drums & Percussion"
        # Computer Audio
        # Keyboard & MIDI
        if "midi" in lcTitle or "keyboard" in lcTitle or "piano" in lcTitle:
            category = "Keyboard & MIDI"
        # Mixers
        if "mixer" in lcTitle:
            category = "Mixers"
        # recorders and PLayers
        if "interface" in lcTitle:
            category = "Recorders & Players"
        # Signal processing
        if ("compressor" in lcTitle and category != "Amps & Effects") or ("equalizer" in lcTitle and category != "Amps & Effects"):
            category = "Signal Processing"
        # Speakers and Monitors
        if "speaker" in lcTitle or "monitor" in lcTitle:
            category = "Speakers & Monitors"

        if category == "":
            category ="Other"

        # Make changes to response for GCUsed
        response.append({'productTitle': title,
                       'productCondition': condition,
                        'productPrice': price,
                        'productLocation': location,
                        'productLink': link,
                        'productCategory': category})
                        # category, ID still needed, description

browser.quit()
# Write response to JSON file
postingsFile = '/Users/NoahKArman/Documents/CSC 3130/WebProject_NoahKarman/JSON/' + today + '.GCUSed.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=True, indent=2)

outfile.close()