from pyrogram import Client
from pyrogram.raw import functions, types
from pyrogram.errors import FloodWait
import asyncio
import os

class Tagger:
    def __init__(self,client: Client, offset: int, channel: str | int) -> None:
        self._client = client
        self.offset = offset or 0
        self.limit = 0
        self.channel = channel
        self.users = []

    async def tag_all(self):
        channel_max_user = await self._client.get_chat_members_count(self.channel)
        while channel_max_user >= len(self.users):
            u = await self.tagger(self._client,len(self.users), self.limit, self.channel)
            if len(self.users) == channel_max_user:
                break
            await asyncio.sleep(2)
        return self.users
    async def tagger(self, client: Client,offset: int, limit: int,channel: str | int):
        users = []
        while True:
            print(len(users))
            try:
                participants = await client.invoke(
                    functions.channels.GetParticipants(
                        channel=await client.resolve_peer(channel),
                        filter=types.ChannelParticipantsSearch(q=""),
                        offset=offset,
                        limit=0,
                        hash=0,
                    )
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
                continue
            await asyncio.sleep(0.3)
            if not participants.participants:
                break 

            users.extend(participants.users)
            offset += limit
        self.users.extend(users)