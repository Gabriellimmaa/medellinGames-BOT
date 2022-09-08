from datetime import datetime
import pytz
from ctypes import util
from email import utils
import json
import random
import string
from time import time
import tweepy
import configparser
import pandas as pd
from connection import MongoDB
from utils import *
import discord

COR = 0xf9eff8
VERDE = 0x66bb6a
VERMELHO = 0xef5350

class Emoji():
    def __init__(self):
        self.errado = '<:errado:778443911617708043>'
        self.certo = '<:certo:778443911974092840>'
        self.sino = '<:sino:1002445350583410689>'
        self.enviar = '<:enviar:785263625224454144>'
        self.on = '<:on:870326706802659338>'
        self.off = '<:off:870326706416791575>'
        self.placa = '<:placa:922369375858737162>'
        self.chassi = '<:chassi:922369375573516350>'
        self.contato = '<:contato:1002445336570232843>'
        self.cor = '<:cor:922369375552544789>'
        self.carro = '<:veiculo:922369375829364816>'
        self.coin = '<:coin:778444693905735681>'
        self.update = '<:update:783476169860579358>'
        self.sirene = '<a:sirene:854510226962907156>'
        self.atencao = '<a:atencao:778757519245180939>'
        self.calendario = '<:calendario:922369375804227584>'
        self.loading = '<a:loading:973202333112623134>'
        self.seta_azul = '<a:seta_azul:973202525756981308>'
        
class getConfig:
    def __init__(self):    
        config = configparser.ConfigParser(interpolation=None)
        config.read('config.ini')

        self.api_key = config['twitter']['api_key']
        self.api_key_secret = config['twitter']['api_key_secret']

        self.access_token = config['twitter']['access_token']
        self.access_token_secret = config['twitter']['access_token_secret']

        self.client_id = config['twitter']['client_id']
        self.client_secret = config['twitter']['client_secret']

        self.bearer_token = config['twitter']['bearer_token']

        self.discord_token = config['discord']['discord_token']

config = getConfig()

def format_hashtag(value: string):
    """
    value: string -> '#value'
    """
    result = ""
    if not value.startswith("#"):
        result += "#"
    result += value
    return result

def key_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))    

def date():
    "return -> dia/mes as horas:minutos"
    time_zone = pytz.timezone("Brazil/East")
    date_time = datetime.now(time_zone)
    date_date = date_time.strftime("%d/%m as %H:%M")
    return date_date


def checkUserTweet(user: discord.Member, valueHastag: str):
    client = tweepy.Client(config.bearer_token)

    response = client.search_recent_tweets(
        query=format_hashtag(valueHastag),
        max_results=100
    )

    # Pega quantas pessoas tal pessoa esta seguindo
    # user = client.get_user(username='biellimappr')
    # c = client.get_users_followers(user.data['id'])
    # print(c.meta['result_count'])

    with open("data.json", "r") as f:
        data = json.load(f)
    try:
        for msg in response.data:
            if data[str(user.id)]['code'] in str(msg):
                return True
    except:
        return False
    return False

def dividirLista(lista: list, qtd: int):
    x = qtd #em quantos pedacos sera divido
    final_list= lambda test_list, x: [test_list[i:i+x] for i in range(0, len(test_list), x)]
    output = final_list(lista, x)
    return output

async def open_account(user: discord.Member):
    check_user = await MongoDB().dbuser.find_one({"_id": str(user.id)})
    if check_user is None:
        insert = {
            "_id": f"{user.id}", "ponto": 0, "vitoria": 0, "derrota": 0, "vip": False, "torcida": False
        }
        await MongoDB().dbuser.insert_one(insert)
    else:
        return False
    return True