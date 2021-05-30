# -*- coding: utf-8 -*-
from random import randint

class Texto_a_array:
    def __init__(self, text_path):
        self.text_path = text_path
        self.text_array = []

    def load_textArray(self):
        print("Cargando array de texto de: "+self.text_path)
        f = open(self.text_path, "r")
        for line in f:
            self.text_array.append(line)

    def get_comment(self):
        if not self.text_array:
            return "Empty:("
        index = randint(0,len(self.text_array)-1)
        return self.text_array[index]
