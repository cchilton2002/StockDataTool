from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# API and Database Configuration
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

# Database Config Dictionary
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}