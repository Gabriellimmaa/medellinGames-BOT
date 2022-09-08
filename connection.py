import motor
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

class MongoDB:
    def __init__(self):
        cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://gabriellima:Y6VuDgg8QNVylIF1@cluster0.polpmg2.mongodb.net/test")

        main = cluster.main
        self.dbuser = main.user
        self.dbtorcida = main.torcida