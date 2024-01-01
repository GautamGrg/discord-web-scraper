from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import locale
import random
import json
import requests

webhook_Url = "your webhook api"
target_Url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&minBedrooms=3&maxPrice=500000&radius=5.0&sortType=6&propertyTypes=detached%2Csemi-detached%2Cterraced&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords='
headers = {'User-Agent': 'Chrome/91.0.4472.124'}

def scrape_timer():
    scrape_interval = 1800
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

    for i in range(1, 24, len(titles)):
        store.append ({
            'title' : (titles[i]),
            'address' : (addresses[i]),
            'description' : (descp[i]),
            'price' : prices[i],
            'date' : dates[i],
            'image' : images[i]
        })
    return store


if __name__ == '__main__':
    listings = house_listing()
    for listing in listings:
        data = {   
        "content" : 'Rightmove listing',
        "embeds" : [{
            "title" : listing["title"],
            "description": f"Price: {listing['price']}",
            "thumbnail" : {"url": listing["image"]}
            }]
        }
    send_Webhook = requests.post (webhook_Url, json=data)
    print (send_Webhook.content)



# print (json.dumps(house_listing(), indent = 2, ensure_ascii=False))
# response = (json.dumps(data, indent = 2, ensure_ascii=False))

# while True:
#     latest_listing = house_listing()
#     print (json.dumps(latest_listing, indent = 2, ensure_ascii=False))
#     time.sleep(scrape_timer())


# response = json.dumps (house_listing(), indent=2, ensure_ascii= False)
# send_Webhook = requests.post (webhook_Url, json=house_listing()) 
# print (send_Webhook.status_code)
# print (send_Webhook.content)

# print (json.dumps(house_listing(), indent=2))

# response = requests.post (webhook_Url, json = data)
# print (response.status_code)
# print (response.content)

    

