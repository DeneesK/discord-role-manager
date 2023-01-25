import asyncio
import logging
import time
import threading

import discord
from discord import utils, Intents, Member, Guild, Role

from config import LOGGER_SETTINGS, TIME_SLEEP
from services import NamesService

logging.basicConfig(**LOGGER_SETTINGS)
logger = logging.getLogger(__name__)


class BotClient(discord.Client):
    def __init__(self, *, 
                 intents: Intents, 
                 name_service: NamesService,
                 server_id: int,
                 roles: dict
                ) -> None:
        super().__init__(intents=intents)
        self.name_service = name_service
        self.server_id = server_id
        self.roles = roles
    
    @staticmethod
    def checking_users(bot: discord.Client, loop: asyncio.BaseEventLoop) -> None:
        while True:
            time.sleep(TIME_SLEEP)
            logger.info('Bot starts checking users')
            _ = loop.create_task(bot.users_add_roles())
            _ = loop.create_task(bot.users_remove_roles())
    
    @property    
    def server_guild(self) -> Guild:
        return self.get_guild(self.server_id)
    
    @property
    def npc_role(self) -> Role:
        return utils.get(self.server_guild.roles, id=self.roles['NPC'])

    async def on_ready(self) -> None:
        logger.info(f'Logged on as {self.user}!')
        loop = asyncio.get_running_loop()
        logger.info(f'Created Thread for additional tasks')
        threading.Thread(target=self.checking_users, args=(self, loop), daemon=True).start()

    async def on_member_join(self, member: Member) -> None:
        logger.info(f'{member.name} joined to the server')

        if self.name_service.check_name(member.name):
            await member.add_roles(self.npc_role)
            logger.info(f'{member.name} gets role')
    
    async def users_remove_roles(self) -> None:
        members = self.server_guild.members
        active_members = self.name_service.get_names()
        to_remove = [user for user in members if not user.name in active_members and self.npc_role in user.roles]
        logger.info(f'{len(to_remove)} users will be removed role NPS')
        [await user.remove_roles(self.npc_role) for user in to_remove]
    
    async def users_add_roles(self) -> None:
        members = self.server_guild.members
        active_members = self.name_service.get_names()
        to_add = [user for user in members if not self.npc_role in user.roles and user.name in active_members]
        logger.info(f'{len(to_add)} users will be added role NPS')
        [await user.add_roles(self.npc_role) for user in to_add]
