from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import locale
import random
import json
import requests

DISCORD_WEBHOOK_PATH = "https://discord.com/api/webhooks/914721010664742943/g-hf_nUM7r1_6aqXaoEEbNoX8cXHgj2eOyiQ5YTtEEI2Gs6ZsuTY3_Lfx7I1MDJylIv6"
target_url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&minBedrooms=2&maxPrice=400000&sortType=6&propertyTypes=detached%2Csemi-detached%2Cterraced&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords='
headers = {'User-Agent': 'Chrome/91.0.4472.124'}

def scrape_timer():
    scrape_interval = 1800
    return scrape_interval


def house_listing():
    response = requests.get(target_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    store = []
    titles = [title.text.strip() for title in soup.find_all('h2', {'class': 'propertyCard-title'})]
    addresses = [address['content'] for address in soup.find_all('meta', {'itemprop' : 'streetAddress'})]
    descp = [description.text for description in soup.find_all('span', {'data-test': 'property-description'})]
    prices = [price.text.strip() for price in soup.find_all('div', {'class' : 'propertyCard-priceValue'})]
    dates = [date.text.split()[-1] for date in soup.findAll('span', {'class':'propertyCard-branchSummary-addedOrReduced'})]
    images = [image['src'] for image in soup.findAll('img', {'itemprop' : 'image'})]

    for i in range(1, 24, len(titles)):
        store.append ({
            'title' : titles[i],
            'address' : addresses[i],
            'description' : descp[i],
            'price' : prices[i],
            'date' : dates[i],
            'image' : images[i]
        })
    return store
    

while True:
    latest_listing = house_listing()
    print (json.dumps(latest_listing, indent = 2, ensure_ascii=False))
    time.sleep(scrape_timer())
    

