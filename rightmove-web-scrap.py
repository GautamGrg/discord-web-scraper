from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import locale
import random
import json
import requests

webhook_Url = "Your discord webhook API"
target_Url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22emmmIrtzQnldW%60hDo%7Ck%40qstWc_iLdtjDwfdChxxAkiHxgrEmvuD~gDwg~Crz~GlauDpnQ%22%7D&sortType=6&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords='
headers = {'User-Agent': 'Chrome/120.0.6099.144'}

def scrape_timer():
    scrape_interval = 30
    return scrape_interval

def house_listing():
    response = requests.get(target_Url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    store = []
    titles = [title.text.strip() for title in soup.find_all('h2', {'class': 'propertyCard-title'})]
    addresses = [address['content'] for address in soup.find_all('meta', {'itemprop' : 'streetAddress'})]
    descp = [description.text for description in soup.find_all('span', {'data-test': 'property-description'})]
    prices = [price.text.strip() for price in soup.find_all('div', {'class' : 'propertyCard-priceValue'})]
    dates = [date.text.split()[-1] for date in soup.findAll('span', {'class':'propertyCard-branchSummary-addedOrReduced'})]
    images = [image['src'] for image in soup.findAll('img', {'itemprop' : 'image'})]

    for i in range(1, 25, len(titles)):
        store.append ({
            'title' : (titles[i]),
            'address' : (addresses[i]),
            'description' : (descp[i]),
            'price' : prices[i],
            'date' : dates[i],
            'image' : images[i]
        })
    # print (store)
    return store

if __name__ == '__main__':
    temp = set()
    while True:
        try:
            discord_POST = house_listing()
            for listing in discord_POST:
                # Create a unique identifier for the current listing
                listing_identifier = f"{listing['title']}"
                # Check if the current listing has been sent recently
                if listing_identifier not in temp:
                    data = {   
                        "content": 'Rightmove listing',
                        "embeds": [{
                            "title": listing["title"],
                            "description": f"Price: {listing['price']}",
                            "thumbnail": {"url": listing["image"]}
                        }]
                    }
                    send_Webhook = requests.post(webhook_Url, json=data)
                    print(f"New listing posted: {listing}")
                    temp.add(listing_identifier)

            # Wait before processing the next set of listings
            # time.sleep(scrape_timer())
        except Exception as err:
            print(err)



    

