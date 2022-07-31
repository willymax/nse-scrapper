import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
print(MONGO_USER)
print(MONGO_PASSWORD)
