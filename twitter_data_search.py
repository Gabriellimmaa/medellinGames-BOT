from ctypes import util
from email import utils
import json
import string
from time import time
import tweepy
import configparser
import pandas as pd
from utils import *
import discord

config = getConfig()

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
        if data[str(user.id)]['hashtag'] in str(msg):
            return True
    return False
