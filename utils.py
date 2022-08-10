import configparser
import random
import string

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