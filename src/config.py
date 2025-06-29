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

with open("../templates/sql_agent_json", "r") as f:
    SYSTEM_PROMPT_TEMPLATE = f.read()

with open("../database/schema.sql", "r") as f:
    DB_SCHEMA = f.read()

KNOWN_ACTIONS = {
    "execute_sql": "execute_sql",
}