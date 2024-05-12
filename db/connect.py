from motor.motor_asyncio import AsyncIOMotorClient
import os 
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():

    url : str = dict(os.environ).get("MONGODB_URL",None)
    if not url:
        raise Exception("Motor client not connected")
    client = AsyncIOMotorClient(url)
    db = client.get_database("fastblog")
    
    return client , db
