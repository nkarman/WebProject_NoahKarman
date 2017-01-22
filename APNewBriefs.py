import requests
from bs4 import BeautifulSoup

# Scrape APNewsBriefs with requests
urlAPNewsBriefs = 'http://hosted.ap.org/dynamic/fronts/HOME?SITE=AP&SECTION=HOME'
pageAPNewsBriefs = requests.get(urlAPNewsBriefs)

# Prepare for parsing APNewsBriefs with BeautifulSoup
soupAPNewsBriefs = BeautifulSoup(pageAPNewsBriefs.content, 'lxml')

position = soupAPNewsBriefs.find('div', class_='ap-newsbriefitem')
headline = position.find('a').string
brief = position.find('span', class_='topheadlinebody').string
apOffice = brief.split(' (AP) ')[0]
fullStory = 'hosted.ap.org' + position.find('a').get('href')
ctime = fullStory.split('CTIME=')[1]

print(headline)
print(brief)
print(apOffice)
print(fullStory)
print(ctime)