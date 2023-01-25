import os
import logging

LOGGER_SETTINGS = {
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "level": logging.INFO
}

TOKEN = os.environ.get('DISCORD_TOKEN')

SERVER_ID = os.environ.get('SERVER_ID')

ROLES = {
    'NPC': os.environ.get('NPC_ID'),
}

SHEET_ID = os.environ.get('SHEET_ID')
COLUMNS = 'Sheet1!B2:B'

TIME_SLEEP = 10