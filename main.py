from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Appwrite client
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')  # Appwrite endpoint
client.set_project(os.getenv("PROJECT_ID")) 
client.set_key(os.getenv("API_KEY_SECRET"))  

databases = Databases(client)
