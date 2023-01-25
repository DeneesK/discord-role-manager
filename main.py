import logging

import discord

from config import TOKEN, SERVER_ID, ROLES, LOGGER_SETTINGS
from services import NamesService
from bot_client import BotClient


logging.basicConfig(**LOGGER_SETTINGS)
logger = logging.getLogger(__name__)

intents = discord.Intents.all()

bot = BotClient(intents=intents,
                server_id=SERVER_ID,
                roles=ROLES,
                name_service=NamesService())


if __name__ == '__main__':
    bot.run(TOKEN)
