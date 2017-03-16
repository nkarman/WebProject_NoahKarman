import requests
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import json

# get today's date
today = str(datetime.datetime.now().date())

# initialize array of responses to be appended to JSON
response = []
browser = webdriver.Chrome('/Users/NoahKArman/Documents/CSC 3130/WebProject_NoahKarman/chromedriver')

baseURLs = [
    'http://used.samashmusic.com/results.php?page=1&type=guitar&cat=electric',
    'http://used.samashmusic.com/results.php?page=1&type=guitar&cat=acoustic',
    'http://used.samashmusic.com/results.php?page=1&type=bass&cat=electric',
    'http://used.samashmusic.com/results.php?page=1&type=bass&cat=acoustic',
    'http://used.samashmusic.com/results.php?page=1&type=drums&cat=acoustic',
    'http://used.samashmusic.com/results.php?page=1&type=drums&cat=snare',
    'http://used.samashmusic.com/results.php?page=1&type=drums&cat=cymbal',
    'http://used.samashmusic.com/results.php?page=1&type=drums&cat=percussion',
    'http://used.samashmusic.com/results.php?page=1&type=amps&cat=guitar',
    'http://used.samashmusic.com/results.php?page=1&type=amps&cat=bass',
    'http://used.samashmusic.com/results.php?page=1&type=keyboards',
    'http://used.samashmusic.com/results.php?page=1&type=live%20sound&cat=wired%20microphones',
    'http://used.samashmusic.com/results.php?page=1&type=live%20sound&cat=mixers',
    'http://used.samashmusic.com/results.php?page=1&type=effects&cat=guitar'
]
# for each page on Sam Ash, generate list of URLS
urlsToParse = []
for url in baseURLs:
    pageNum = 1

    # get number of pages
    pageOfNum = requests.get(url)
    soupNum = soupSA = BeautifulSoup(pageOfNum.content, 'lxml')
    finalNumPosition = soupNum.find('div', class_='gear_list')
    finalNum = 1

    try:
        finalNumURL = finalNumPosition.contents[24].contents[17].attrs['href']
        [trash,finalNum] = finalNumURL.split('page=')
        try:
            finalNum = int(finalNum[:2])
        except(ValueError):
            finalNum = int(finalNum[:1])
    except (IndexError, AttributeError, ValueError):
        print(url + " failed to get final pageNum")
        pageNum = 1
    while pageNum <= int(finalNum):
        [url1, url2] = url.split("page=")
        theURL = url1 + 'page=' +str(pageNum) + url2[1:]
        urlsToParse.append(theURL)
        print(theURL)
        pageNum = pageNum + 1

for url in urlsToParse:
    pageSA = browser.get(url)
    soupSA = BeautifulSoup(browser.page_source, 'lxml')

    for position in soupSA.find_all('div', class_='gear'):
        title = 'n/a'
        price = 'n/a'
        location = 'n/a'
        productLink = 'n/a'
        category = 'n/a'
        productId= 'n/a'
        description = 'n/a'
        try:
            title = position.contents[1].contents[0].string
            description = position.contents[1].contents[2].string
            price = position.contents[2].contents[0].contents[0]
            location = position.contents[2].contents[2].contents[0].contents[0]
            productRef = position.contents[2].contents[4].contents[0].attrs['href']
            [trash, productID] = productRef.split("id=")
            productLink = 'http://used.samashmusic.com/item.php?id=' + productID
        except(IndexError):
            print('ruh-roh raggy, index out of bounds!')

        if ('guitar' in url or 'bass' in url) and 'effects' not in url:
            category = 'Guitar & Bass'
        if 'microphones' in url:
            category = 'Microphones'
        if 'effects' in url or 'amps' in url:
            category = 'Amps & Effects'
        if 'mixers' in url:
            category = 'Mixers'
        if 'keyboards' in url:
            category = 'Keyboard & MIDI'
        if 'drums' in url:
            category = 'Drums & Percussion'
        print(title, price, location, productID)
        response.append({'productTitle': title,
                         'productPrice': str(price),
                         'productLocation': str(location),
                         'productLink': str(productLink),
                         'productCategory': str(category),
                         'productID': str(productID),
                         'productDescription': str(description)})


            # store each field into json response
browser.quit()

# write JSON file
postingsFile = '/Users/NoahKArman/Documents/CSC 3130/WebProject_NoahKarman/JSON/' + today + '.SA_used.json'

with open(postingsFile, 'w') as outfile:
    json.dump(response, outfile, sort_keys=True, indent=2)

outfile.close()