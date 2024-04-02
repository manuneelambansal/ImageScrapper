from pymongo.mongo_client import MongoClient
from bs4 import BeautifulSoup
import requests
import os

query = 'Phones'

url = f"https://www.google.com/search?q={query}&sxsrf=AJOqlzUuff1RXi2mm8I_OqOwT9VjfIDL7w:1676996143273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiq-qK7gaf9AhXUgVYBHYReAfYQ_AUoA3oECAEQBQ&biw=1920&bih=937&dpr=1#imgrc=1th7VhSesfMJ4M"

response = requests.get(url)

if response.status_code == 200:

    save_directory = "images/"

    # create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')
    del images[0]
    img_data =[]
    
    for index,image_tag in enumerate(images):
        # get the image source URL
        image_url = image_tag['src']
        #print(image_url)
        
        # send a request to the image URL and save the image
        image_data = requests.get(image_url).content
        mydict={"Index":index,"Image":image_data}
        img_data.append(mydict)
        # print((image_data))
        with open(os.path.join(save_directory, f"{query}_{index}.jpg"), "wb") as f:
            f.write(image_data)


uri = "mongodb+srv://mbansal1820:MongoDB7744@cluster0.jv3xc3i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client['image_scrap']
collection = db['image_scrap_data']

collection.insert_many(img_data)