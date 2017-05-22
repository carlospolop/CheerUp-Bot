# -*- coding: utf-8 -*-
import requests
from random import randint
from bs4 import BeautifulSoup
import urllib
import threading

class Imagenes:
    def __init__(self, searches, image_path, isGif=False):
        self.images_urls = []
        self.load_page = 0
        self.searches = searches
        self.isGif = isGif
        self.image_path = image_path

    def save_image(self, url):
        img_data = requests.get(url).content
        with open(self.image_path, 'wb') as image:
            image.write(img_data)

    def load_imagesUrls(self):
        print "Cargando imagenes..."
        url = "https://www.ecosia.org/images?"
        for search in self.searches:
            getVarP = { 'p': str(self.load_page) }
            getVarQ = { 'q': str(search) }
            getUrl = str(url) + str(urllib.urlencode(getVarP)) + "&" + str(urllib.urlencode(getVarQ))
            r = requests.get(getUrl)
            print "Request realizada: "+str(getUrl)
            soup = BeautifulSoup(r.content,'html5lib')
            imageUrls_loaded = soup.find_all('a', {'class':"image-result js-image-result"})
            for url_image in imageUrls_loaded:
                #print url_image
                #if(self.isGif and (".gif" in url_image)):
                self.images_urls.append(url_image["href"])

        self.load_page += 1

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
