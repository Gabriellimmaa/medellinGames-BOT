import motor
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

class MongoDB:
    def __init__(self):
        cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

        main = cluster.main
        self.dbuser = main.user
        self.dbtorcida = main.torcida