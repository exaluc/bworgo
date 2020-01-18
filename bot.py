#!/usr/bin/env python3

import json
import time
import datetime
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup

headers_epic = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
}

headers_discord = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
}

# epic 

req_epic = request.Request(url='https://www.epicgames.com/store/fr/free-games',
                      headers=headers_epic,
                      method='GET')


# discord 

WEBHOOK_URL = ''

def set_timestamp(timestamp=str(datetime.datetime.utcfromtimestamp(time.time()))):
    """
    set timestamp
    """
    return timestamp

payload = {
  "embeds": [{
    "title": "EPIC GAMES",
    "description": "Horace est un jeu de plates-formes immense qui repousse les limites du genre et dans lequel on suit l'histoire passionnante d'un petit robot qui découvre la vie, l'univers et Douglas Adams. \n\n [**HORACE**](https://www.epicgames.com/store/fr/product/horace/home)",
    "url": "https://www.epicgames.com/store/fr/free-games",
    "color": 30207,
    "timestamp": set_timestamp(),
    "footer": {
      "icon_url": "http://dreamer.fr/discord/ceas.png",
      "text": "disponible jusqu'au : 22 Janv à 17h"
    },
    "image": {
      "url": "https://cdn1.epicgames.com/epic/offer/EGS_PaulHelmanSeanScapelhorn_Horace_G1A_01-1920x1080-12c8bea4a4abedacf097f3e508f11594.jpg"
    },
  }]
}


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
    print(epic.status)
    print(epic.reason)
    print(epic.headers)
except HTTPError as e:
    print('ERROR')
    print(e.reason)
    print(e.hdrs)
    print(e.file.read())