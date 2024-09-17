import requests
import json
import config

def get_offset_url(url, offset = 0):
    url = url.replace('offset','offset*').split('*')
    return url[0] + f'={offset}' + url[1][2:]


def get_weapons_data(url):
    data = requests.get(url = url).json()
    items = data['items']
    weapons = []
    names = set()
    for weapon in items:
        if weapon['links'] == {}: continue
        name = weapon['asset']['names']['full']
        if name in names: continue
        names.add(name)
        link = weapon['links']['3d']
        if link is None:
            link = f'https://wiki.cs.money/keys/{name.lower().replace(' ', '-').replace('.','').replace('|','').replace('(','').replace(')','').replace('--','-')}'
        price = weapon['pricing']
        price = [price['priceBeforeDiscount'], round(price['discount']*100) if price['discount'] < 0 else 0]

        weapons.append([name,link,price])
    
    return weapons