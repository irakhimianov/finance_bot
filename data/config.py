import os
from dotenv import load_dotenv


load_dotenv()

ADMINS = [396263809, 5649071858]
TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN_ID')
GEO_TOKEN = os.getenv('GEO_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
EXCHANGERATE_TOKEN = os.getenv('EXCHANGERATE_TOKEN')

PG_DB = os.getenv('PG_DB')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
