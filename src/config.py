from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)

API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL")
MODEL = os.environ.get("MODEL")

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))

CHAINLIT_DB_NAME = os.environ.get("CHAINLIT_DB_NAME")
CHAINLIT_DB_USER = os.environ.get("CHAINLIT_DB_USER")
CHAINLIT_DB_PASSWORD = os.environ.get("CHAINLIT_DB_PASSWORD")
CHAINLIT_DB_HOST = os.environ.get("CHAINLIT_DB_HOST")
CHAINLIT_DB_PORT = os.environ.get("CHAINLIT_DB_PORT")

with open("templates/sql_agent_json.txt", "r") as f:
    SYSTEM_PROMPT_TEMPLATE = f.read()

with open("database/scripts/schema.sql", "r") as f:
    DB_SCHEMA = f.read()