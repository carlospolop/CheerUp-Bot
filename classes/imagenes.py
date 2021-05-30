# -*- coding: utf-8 -*-
import os
import requests
from random import randint
import threading
from time import sleep

class Imagenes:
    def __init__(self, searches, image_path, isGif=False):
        self.images_urls = []
        self.load_page = 0
        self.searches = searches
        self.isGif = isGif
        self.image_path = image_path

    def save_image(self, url):
        img_data = requests.get(url).content
        os.system(f"ls {self.image_path}")
        with open(self.image_path, 'wb') as image:
            image.write(img_data)

    def load_imagesUrls(self):
        print("Cargando imagenes...")
        url = "https://api.unsplash.com/search/photos"
        for search in self.searches:
            params = {
                "query": search,
                "per_page": "30",
                "order_by": "latest",
                "client_id": os.getenv('UNSPLASH_ACCESS_KEY')
            }
            r = requests.get(url, params=params)
            self.images_urls += [u['urls']['small'] for u in r.json()['results']]
            sleep(1)

    def get_imagesUrl(self):
        if not self.images_urls:
            self.load_imagesUrls()
            self.get_imagesUrl()
        index = randint(0,len(self.images_urls)-1)
        url = self.images_urls[index]
        del self.images_urls[index]
        self.save_image(url)

    def get_path(self):
        t = threading.Thread(target=self.get_imagesUrl).start()
        return self.image_path
