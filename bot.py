# -*- coding: utf-8 -*-

#hola - Saluda
#start - Hello
#ayuda - Responde
#help - Response
#chiste - Cuenta un chiste
#animame - Envia una imagen de animo
#cheer_up - Send a cheer up picture
#comida - Envia una imagen de una buena comida
#food - Send an image of a tasty food
#animal - Envia una imagen de un animalillo
#animal - Send a picture of a cute animal
#especial - Envia una imagen especial
#special - Send a special picture
#sticker - Envia un sticker
#sticker - Send a sticker
#sorprendeme - Te sorprenderá
#surprise - It will surprise you
#elimina_stickers - Elimina los stickers guardados
#remove_stickers - Remove all the stickers
#es_mi_cumple - Felicidades!!
#its_my_birthday - Congratulations!!
#examen - Ohh, a ver si te animo
#exam - Ohh, let my cheer you up



import telebot # Librería de la API del bot.
#from telebot import types # Tipos para la API del bot.
import requests
import os
import random
import shutil
from random import randint
import pathlib

from classes.chistes import Chistes
from classes.imagenes import Imagenes
from classes.texto_a_array import Texto_a_array
#https://github.com/eternnoir/pyTelegramBotAPI#writing-your-first-bot

#time.sleep(10)

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN')) # Creamos el objeto de nuestro bot.

chats = dict()

chistes = Chistes()
chistes.load_chistes()

absPath = pathlib.Path(__file__).parent.absolute()
print(absPath)

texts_folder = os.path.join(absPath, "texts/")
birthday_path = os.path.join(texts_folder, "birthday.txt")
if (os.path.isfile(birthday_path)):
    birthday_array = Texto_a_array(birthday_path)
    birthday_array.load_textArray()

examen_path = os.path.join(texts_folder, "examen.txt")
if (os.path.isfile(examen_path)):
    examen_array = Texto_a_array(examen_path)
    examen_array.load_textArray()

imagenes_folder = os.path.join(absPath, "images/")
imagenes_animo = Imagenes(["animo", "cheer up", "happiness", "super happy"], imagenes_folder+"animo.jpg")
imagenes_comida = Imagenes(["dessert", "cake", "hamburguer", "pizza", "ribs", "milkshakes", "cocktail"], imagenes_folder+"comida.jpg")
imagenes_animales = Imagenes(["cute animals", "cute cats", "cute dogs", "baby bear", "cute rabbit"], imagenes_folder+"animal.jpg")
imagenes_especiales = Imagenes(["minion", "winnie the pooh", "pingu", "sponge bob"], imagenes_folder+"special.jpg")
imagenes_gif = Imagenes(["funny gifs"], imagenes_folder+"temp.gif", True)

imagenes_animo.load_imagesUrls()
imagenes_animo.get_imagesUrl()
imagenes_comida.load_imagesUrls()
imagenes_comida.get_imagesUrl()
imagenes_animales.load_imagesUrls()
imagenes_animales.get_imagesUrl()
imagenes_especiales.load_imagesUrls()
imagenes_especiales.get_imagesUrl()
#imagenes_gif.load_imagesUrls()

print(absPath)
stickers_folder = os.path.join(absPath, "stickers/")
def create_folders():
    if not os.path.exists(stickers_folder):
        print(f"Creating {stickers_folder}")
        os.makedirs(stickers_folder)
    if not os.path.exists(imagenes_folder):
        print(f"Creating {imagenes_folder}")
        os.makedirs(imagenes_folder)
    if not os.path.exists(texts_folder):
        print(f"Creating {texts_folder}")
        os.makedirs(texts_folder)

def always(message):
    pass
    """print(message.chat.first_name)
    #print(message.chat.id)
    #chats[message.chat.first_name] = message.chat #Add new chat
    #bot.forward_message(mId, message.chat.id, message.message_id) #FW
    """

def send_image(message, path):
    always(message)
    if not os.path.exists(path):
        bot.send_message(message.chat.id, "Cargando imagen...\nPrueba en unos segundos")
    else:
        image = open(path, 'rb')
        bot.send_photo(message.chat.id, image)
        #bot.send_photo(message.chat.id, "FILEID")

def send_gif(message, url):
    img_data = requests.get(url).content
    with open('temp.gif', 'wb') as image:
        image.write(img_data)
    image = open('temp.gif', 'rb')
    bot.send_document(message.chat.id, image)
    bot.send_document(message.chat.id, "FILEID")

##COMMANDS
# Handles all text messages that contains the commands '/start' or '/hola'
@bot.message_handler(commands=['start', 'hola'])
def send_welcome(message):
    always(message)
    bot.reply_to(message, "Hola, que tál?")

@bot.message_handler(commands=['help','ayuda'])
def send_help(message):
    always(message)
    bot.reply_to(message, "Todos necesitamos ayuda alguna vez, cuéntame")

@bot.message_handler(commands=['chiste'])
def send_chiste(message):
    always(message)
    bot.send_message(message.chat.id, chistes.get_chiste())

@bot.message_handler(commands=['animame', 'cheer_up'])
def send_imageCheerUp(message):
    path = imagenes_animo.get_path()
    send_image(message,path)

@bot.message_handler(commands=['comida', 'food'])
def send_imageFood(message):
    path = imagenes_comida.get_path()
    send_image(message,path)

@bot.message_handler(commands=['animal'])
def send_imageAnimal(message):
    path = imagenes_animales.get_path()
    send_image(message,path)

@bot.message_handler(commands=['especial', 'special'])
def send_imageSpecial(message):
    path = imagenes_especiales.get_path()
    send_image(message,path)

@bot.message_handler(commands=['gif'])
def send_gifCommand(message):
    #url = imagenes_gif.get_imagesUrl()
    #send_gif(message,url)
    pass

@bot.message_handler(commands=['sticker'])
def send_stickerCommand(message):
    always(message)
    for (dirpath, dirnames, filenames) in os.walk(stickers_folder):
        if filenames:
            sticker = stickers_folder + random.choice(filenames)
            while not(".webp" in sticker):
                sticker = stickers_folder + random.choice(filenames)
            sti = open(sticker, 'rb')
            bot.send_sticker(message.chat.id, sti)
            bot.send_sticker(message.chat.id, "FILEID")
            break

@bot.message_handler(commands=['remove_stickers','elimina_stickers'])
def remove_stickers(message):
    always(message)
    shutil.rmtree(stickers_folder)
    os.makedirs(stickers_folder)

@bot.message_handler(commands=['sorprendeme', "surprise"])
def send_surprise(message):
    commands = ['chiste', 'animame', 'comida', 'animal', 'especial', 'sticker']
    index = randint(0,len(commands)-1)
    if index == 0:
        send_chiste(message)
    elif index == 1:
        send_imageCheerUp(message)
    elif index == 2:
        send_imageFood(message)
    elif index == 3:
        send_imageAnimal(message)
    elif index == 4:
        send_imageSpecial(message)
    else:
        send_stickerCommand(message)

@bot.message_handler(commands=['es_mi_cumple','its_my_birthday'])
def birthday(message):
    always(message)
    comment = birthday_array.get_comment()
    bot.send_message(message.chat.id, comment)

@bot.message_handler(commands=['examen','exam'])
def exam(message):
    always(message)
    comment = examen_array.get_comment()
    bot.send_message(message.chat.id, comment)

@bot.message_handler(commands=['enviar_mensaje_a','send_message_to'])
def send_message_to(message):
    always(message)
    if(message.text):
        text_split = message.text.split(' ', 2)
        if ((chats[text_split[1]] is not None) and text_split[2]):
            bot.send_message(chats[text_split[1]], text_split[2])

@bot.message_handler(commands=['enviar_sorpresa','send_surprise']) #/enviar_sorpresa QUIEN QUÉ NO FUNCIONA
def programar(message):
    always(message)
    if(message.text):
        text_split = message.text.split()
        if ((chats[text_split[1]]is not None) and text_split[2]):
            message.chat = chats[text_split[1]]
            #message["from"] = chats[text_split[1][1]]
            message.text = text_split[2]
            echo_all(message)

##END COMMANDS

# Handles all sent sticker
# Guarda el sticker en una carpeta
@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    file_path = bot.get_file(message.sticker.file_id).file_path
    url = 'https://api.telegram.org/file/bot{0}/{1}'.format(os.getenv('TELEGRAM_BOT_TOKEN'), file_path)
    print("Descargando sticker: ")+file_path
    sticker = requests.get(url)
    with open(file_path, 'wb') as new_sticker: #Lo guarda en la carpeta stickers/ID.webp
        new_sticker.write(sticker.content)

# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
	bot.reply_to(message, "Qué interesante!")

#Text
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if "hola" in message.text:
        send_welcome(message)
    elif "ayuda" == message.text:
        send_help(message)
    elif "chiste" == message.text:
        send_chiste(message)
    elif "animame" == message.text:
        send_imageCheerUp(message)
    elif "comida" == message.text:
        send_imageFood(message)
    elif "animal" == message.text:
        send_imageAnimal(message)
    elif "especial" == message.text:
        send_imageSpecial(message)
    elif "gif" == message.text:
        send_gifCommand(message)
    elif "sticker" == message.text:
        send_stickerCommand(message)
    elif "elimina_stickers" == message.text:
        remove_stickers(message)
    elif "sorprendeme" == message.text:
        send_surprise(message)
    elif "examen" == message.text:
        exam(message)
    elif "es mi cumple" == message.text:
        birthday(message)
    else:
	    #bot.send_message(message.chat.id, message.text) Repite lo dicho
        bot.send_message(message.chat.id, "cuentame más")
        always(message)



#def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
#    for m in messages: # Por cada dato 'm' en el dato 'messages'
#        if m.content_type == 'text': # Filtramos mensajes que sean tipo texto.
#            cid = m.chat.id # Almacenaremos el ID de la conversación.
#            bot.send_message("hola", cid)
#            print "[" + str(cid) + "]: " + m.text # Y haremos que imprima algo parecido a esto -> [52033876]: /start

#bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.

def start_listening():
    try:
        bot.polling(none_stop=True) # Con esto, le decimos al bot$
    except Exception as e:
        print("Error in bot polling: "+str(e))
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print("Second error: "+str(e))

def main():
    create_folders()
    print("Listening...")
    start_listening()

if __name__ == "__main__":
    main()
