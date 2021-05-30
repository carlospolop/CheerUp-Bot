# -*- coding: utf-8 -*-
import requests
from random import randint
from bs4 import BeautifulSoup
import re

class Chistes:
    def __init__(self):
        self.chistes = []
        self.loaded_pages = []
    
    def load_chistes(self):
        print("Cargando chistes...")
        n_pagina = randint(1,153)
        while (n_pagina in self.loaded_pages):
            n_pagina = randint(1,153)
        r = requests.get('http://www.1000chistes.com/pagina/'+str(n_pagina))
        self.loaded_pages.append(n_pagina)
        soup = BeautifulSoup(r.content,'lxml')
        chistes_loaded = soup.find_all('p', {'class':"texto", 'itemprop':"articleBody"})
        for chiste in chistes_loaded:
            self.chistes.append(re.sub('<.*?>', '', str(chiste)))
    
    def get_chiste(self):
        if not self.chistes:
            self.load_chistes()
            self.get_chiste()
        return self.chistes.pop()
