import requests
import datetime

today = str(datetime.datetime.now()).split(' ')[0]

sites = {'Reverb': 'http://reverb.com/marketplace/',
         'SweetWater':'http://www.sweetwater.com/'}

for name, link in sites.items():
    response = requests.get(link)
    html = response.content

    fileName = today + '.' + name + '.html'
    outfile = open(fileName, "wb")
    outfile.write(html)
    outfile.close()http://www.guitarcenter.com