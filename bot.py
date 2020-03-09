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
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
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
options.headless = True
browser = webdriver.Firefox(options=options)
browser.get(url)
sleep(2)
html = browser.page_source
jeux_gratos = browser.find_element(By.XPATH, "/html/body/div/div/div[4]/div[1]/div[4]/div[2]/div")
#print(jeux_gratos.text)
html = jeux_gratos.get_attribute('innerHTML')

soup = BeautifulSoup(html, "lxml")
urls = []
for link in soup.find_all('a'):
    l = link.get('href')
    # print(l)
    urls.append(l)

images = []
for img in soup.find_all('img'):
    i = img.get('data-image')
    # print(i)
    images.append(i)

infos = []
for nom in soup.find_all('span'):
    n = nom.get_text()
    infos.append(n)

#A = ['Gratuit maintenant', 'Offworld Trading Company', 'Gratuit maintenant - 12 mars à 16:00', 'Gratuit maintenant - 12 mars à 16:00', 'Gratuit maintenant', 'GoNNER', 'Gratuit maintenant - 12 mars à 16:00', 'Gratuit maintenant - 12 mars à 16:00', 'Bientôt disponible', 'Anodyne 2: Return to Dust', 'Gratuit 12 mars - 19 mars', 'Gratuit 12 mars - 19 mars', 'Bientôt disponible', 'A Short Hike', 'Gratuit 12 mars - 19 mars', 'Gratuit 12 mars - 19 mars', 'Bientôt disponible', 'Mutazione', 'Gratuit 12 mars - 19 mars', 'Gratuit 12 mars - 19 mars']
noms = split_list(infos, wanted_parts=5)

#images = ['https://cdn1.epicgames.com/epic/offer/EGS_MohawkGames_OffworldTradingCompany_S4-510x680-5c715e53a4447c2dc5429fc0c76d74f6.jpg?h=854&resize=1&w=640', 'https://cdn1.epicgames.com/epic/offer/EGS_ART_IN_HEART_GONNER_S2_DESCRIPTION-1280x1440-27d8b7fa65e5b130cbcf759a6c1204a9.jpg?h=854&resize=1&w=640', None, 'https://cdn1.epicgames.com/epic/offer/EGS_Anodyne2ReturntoDust_AnalgesicProductions_S2-860x1148-aac459f705d6d93488ac320c6433bdd3.jpg?h=854&resize=1&w=640', 'https://cdn1.epicgames.com/epic/offer/EGS_AShortHike_AdamRobinsonYu_S2-860x1148-cd5bb99336010e748745f1b33f45670d.jpg?h=854&resize=1&w=640', 'https://cdn1.epicgames.com/epic/offer/EGS_Mutazione_DieGuteFabrik_S4-510x680-85ee3c8f3c08de0da2068e6d6441b253.jpg?h=854&resize=1&w=640']
#urls = ['/store/fr/product/offworld-trading-company/home', '/store/fr/product/gonner/home', '/store/fr/product/anodyne-2-return-to-dust/home', '/store/fr/product/a-short-hike/home', '/store/fr/product/mutazione/home']

donnees = {}

for d, i, u in zip(noms, images, urls):
    #print(d, i, u)
    donnee = {}
    etat = d[0]
    if etat == 'Gratuit maintenant':
        donnee['etat'] = etat
        nom = d[1]
        donnee['nom'] = nom
        dtfin = d[2]
        donnee['dtfin'] = dtfin
        image = i
        donnee['image'] = image
        url = 'https://www.epicgames.com'+u
        donnee['url'] = url
        #print(donnee)
        donnees.update(donnee)
        #print(donnees)
        payload = {
        "embeds": [{
            "title": f"{donnees.get('nom')}  👉  {donnees.get('etat')}",
            "description": f"Offre jeu gratuit Epic Games. \n\n [**{donnees.get('nom')}**]({donnees.get('url')})",
            "url": donnees.get('url'),
            "color": 30207,
            "timestamp": set_timestamp(),
            "footer": {
            "icon_url": "http://dreamer.fr/discord/ceas.png",
            "text": donnees.get('dtfin')
            },
            "image": {
            "url": donnees.get('image')
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