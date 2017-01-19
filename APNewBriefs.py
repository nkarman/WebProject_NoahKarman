import requests
from bs4 import BeautifulSoup

# Scrape APNewsBriefs with requests
urlAPNewsBriefs = 'http://hosted.ap.org/dynamic/fronts/HOME?SITE=AP&SECTION=HOME'
pageAPNewsBriefs = requests.get(urlAPNewsBriefs)

# Prepare for parsing APNewsBriefs with BeautifulSoup
soupAPNewsBriefs = BeautifulSoup(pageAPNewsBriefs.content, 'lxml')

position = soupAPNewsBriefs.find('location of news brief in html')
headline = 'location of headline in html'
brief = 'location of brief in html'
apOffice = 'location of apOffice in html'
fullStory = 'location of fullStory in html'
ctime = 'location of ctime in html'

print(headline)
print(brief)
print(apOffice)
print(fullStory)
print(ctime)