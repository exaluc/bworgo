import json
import time
import datetime
import requests
from urllib import request, response, error, parse
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

headers_discord = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0'
}

WEBHOOK_URLS = ['']

def set_timestamp(timestamp=str(datetime.datetime.utcfromtimestamp(time.time()))):
    """
    set timestamp
    """
    return timestamp

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

url = "https://www.epicgames.com/store/fr/free-games"
options = Options()
options.headless = False
browser = webdriver.Firefox(options=options)
browser.get(url)
sleep(2)
html = browser.page_source
jeux_gratos = browser.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/main/div[3]/div/div/div/div/div[3]/span")
html = jeux_gratos.get_attribute('innerHTML')
soup = BeautifulSoup(html, "lxml")


def getUrls():
    urls = []
    for link in soup.find_all('a'):
        l = link.get('href')
        print(l)
        urls.append(l)
    return urls

def getImagesAndName():
    res = []
    for img in soup.find_all('img'):
        i = img.get('data-image')
        t = img.get('alt')
        j = {"image": f"{i}", "name": f"{t}"}
        res.append(j)
    return res

infos = []
for nom in soup.find_all('span'):
    n = nom.get_text()
    print(n)
    infos.append(n)

dispo = split_list(infos, wanted_parts=5)


zipe = zip(dispo, getImagesAndName(), getUrls())

listeJeux = []
for typeInfo, jsonInfo, urlInfo in zipe:
    jTpl = {"infoDispo": f"{typeInfo[0]}", "dtDispo": f"{typeInfo[1]}", "url": f"https://www.epicgames.com{urlInfo}"}
    jTpl.update(jsonInfo)
    listeJeux.append(jTpl)



for jeu in listeJeux:
    payload = {
        "embeds": [{
            "title": f"{jeu.get('name')}  👉  {jeu.get('infoDispo')}",
            "description": f"Offre jeu gratuit Epic Games. \n\n [**{jeu.get('name')}**]({jeu.get('url')})",
            "url": jeu.get('url'),
            "color": 30207,
            "timestamp": set_timestamp(),
            "footer": {
            "text": jeu.get('dtDispo')
            },
            "image": {
            "url": jeu.get('image')
            },
        }]
        }
    print(payload)
    for WEBHOOK_URL in WEBHOOK_URLS:
        req_discord = request.Request(url=WEBHOOK_URL,
                        data=json.dumps(payload).encode('utf-8'),
                        headers=headers_discord,
                        method='POST')

        try:
            discord = request.urlopen(req_discord)
            print('-------------------------------')
            print(discord.status)
            print(discord.reason)
            print(discord.headers)
            print('-------------------------------')
        except HTTPError as e:
            print('ERROR')
            print(e.reason)
            print(e.hdrs)
            print(e.file.read())

browser.quit()