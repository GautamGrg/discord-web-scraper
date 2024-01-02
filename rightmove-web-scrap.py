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

# if __name__ == '__main__':
#     # temp = set()
#     while True:
#         try:
#             temp = set()
#             discord_POST = house_listing()
#             for listing in discord_POST:
#                 data = {   
#                     "content": 'Rightmove listing',
#                     "embeds": [{
#                         "title": listing["title"],
#                         "description": f"Price: {listing['price']}",
#                         "thumbnail": {"url": listing["image"]}
#                     }]
#                 }
#                 # listing_data = response.json().get('data', {}).get('listing', {})
#                 # listing_identifier = response.json().get('title')
#                 # listing_data = response.strip().get({'embeds': 'title'})
#                 # listing_identifier = f"{listing_data.get('title')}_{listing_data.get('address')}"
#                 if listing not in temp:
#                     send_Webhook = requests.post(webhook_Url, json=data)
#                     temp.add(send_Webhook)
#                 else:
#                     print("Duplicate listing, not posting to Discord.")
#             # time.sleep(scrape_timer())
#         except Exception as err:
#             print(err)
        
# def payload():
#     try:
#         listings = house_listing()
#         responses = []
#         for listing in listings:
#             data = {   
#                 "content": 'Rightmove listing',
#                 "embeds": [{
#                     "title": listing["title"],
#                     "description": f"Price: {listing['price']}",
#                     "thumbnail": {"url": listing["image"]}
#                 }]
#             }
#         #     send_Webhook = requests.post(webhook_Url, json=data)
#         #     responses.append(send_Webhook)
#         # return responses
#     except Exception as err:
#         print(err)

# print (payload())
            

# def payload():
#     try:
#         listings = house_listing()
#         response = []
#         for listing in listings:
#             data = {   
#             "content" : 'Rightmove listing',
#             "embeds" : [{
#                 "title" : listing["title"],
#                 "description": f"Price: {listing['price']}",
#                 "thumbnail" : {"url": listing["image"]}
#             }]
#             }
#             send_Webhook = requests.post(webhook_Url, json=data)
#             response.append(send_Webhook)
#         return response
#     except Exception as err:
#         print (err)

# if __name__ == '__main__':
#     temp = set()
#     discord_POST = payload()
#     print (discord_POST)
#     while True:
#         for response in discord_POST:
#             listing_identifier = (f"{discord_POST.get('title')}")
#             if listing_identifier not in temp:
#                 temp.add(listing_identifier)
    



            # if i not in temp:
            #     temp.append(i)
            #     send_Webhook = requests.post(webhook_Url, json=i)
            # else:
            #     pass
    #print (discord_POST.status_code)







    # listings = house_listing()
    # for listing in listings:
    #     data = {   
    #     "content" : 'Rightmove listing',
    #     "embeds" : [{
    #         "title" : listing["title"],
    #         "description": f"Price: {listing['price']}",
    #         "thumbnail" : {"url": listing["image"]}
    #         }]
    #     }
    # send_Webhook=requests.post(webhook_Url, json=data)
    # time.sleep(scrape_timer())
    # while True: 
    #     if send_Webhook != send_Webhook:
    #         send_Webhook=requests.post(webhook_Url, json=data)
    #         time.sleep(scrape_timer())
    #     else:
    #         continue

        
        # while True: 
        #     if send_Webhook != send_Webhook:
        #         send_Webhook=requests.post(webhook_Url, json=data)
        #         time.sleep(scrape_timer())
        #     else:
        #         continue


   

            

    
    
    # else:
    #     while True:
    #         send_Webhook = requests.post (webhook_Url, json=data)
    #         time.sleep(scrape_timer())
        # print (send_Webhook.status_code)
        # print (send_Webhook.content)



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

    

