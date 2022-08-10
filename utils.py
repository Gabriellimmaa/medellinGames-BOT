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
from utils import *
import discord

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
    for msg in response.data:
        if data[str(user.id)]['code'] in str(msg):
            return True
    return False