import requests
import datetime

today = str(datetime.datetime.now()).split(' ')[0]

# Library of Used Instruments and Music gear
sites = {'Reverb': 'https://reverb.com/marketplace?condition=used',
         'SweetWater': 'https://tradingpost.sweetwater.com',
         'GuitarCenter': 'http://www.guitarcenter.com/Used/'}

for name, link in sites.items():
    response = requests.get(link)
    html = response.content

    fileName = today + '.' + name + '.html'
    outfile = open(fileName, "wb")
    outfile.write(html)
    outfile.close()