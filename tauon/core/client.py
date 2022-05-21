from pyrogram import Client as Base
import importlib
import os
from tauon.logger import logging

_LOG = logging.getLogger(__name__)


class Client(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def download_plugin(self):
        async for i in self.search_messages(chat_id="@TauonPlugin", query="@TauonPlugin"):
            if (
                i.document
                and i.document.file_name.endswith(".py")
                and "@TauonPlugin" in i.document.caption
            ):
                await i.download(i.document, f"tauon/plugins/{i.document}")

    async def get_all_plugins(self):
        if not os.path.exists("downloads"):
            os.mkdir("downloads")
        plugins = []
        await self.download_plugin()
        for i in os.listdir("tauon/plugins/"):
            if i.endswith(".py"):
                plugins.append(i)

    async def import_plugins(self):
        for i in os.listdir("tauon/plugins/"):
            if i.endswith(".py"):
                importlib.import_module(f"tauon.plugins.{i[:-3]}")
        print("Imported plugins")

    async def start(self):
        print("Client Started")
        _LOG.info("Client Started")
        await super().start()
        await self.import_plugins()

    async def stop(self):
        print("Client Stoped")
        _LOG.info("Client Stoped")
        await super().stop()
