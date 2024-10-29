from pathlib import Path

import aiofiles
import ujson
from httpx import AsyncClient

ASSETS_PATH = Path("assets")
ASSETS_GS_PATH = ASSETS_PATH / "genshin.json"
ASSETS_MC_PATH = ASSETS_PATH / "mc.json"


class AssetsGen:
    def __init__(self):
        self.client = AsyncClient(follow_redirects=True)

    async def fetch(self, url: str) -> dict:
        response = await self.client.get(url)
        return response.json()

    # gs

    async def fetch_avatars_gs(self):
        data = await self.fetch("https://gi.yatta.moe/api/v2/chs/avatar")
        new_data = {}
        for item in data["data"]["items"].values():
            new_data[item["name"]] = (
                f"https://gi.yatta.moe/assets/UI/{item['icon']}.png"
            )
        return new_data

    async def fetch_weapons_gs(self):
        data = await self.fetch("https://gi.yatta.moe/api/v2/chs/weapon")
        new_data = {}
        for item in data["data"]["items"].values():
            new_data[item["name"]] = (
                f"https://gi.yatta.moe/assets/UI/{item['icon']}.png"
            )
        return new_data

    async def main_gs(self):
        data = {}
        avatars = await self.fetch_avatars_gs()
        data.update(avatars)
        weapons = await self.fetch_weapons_gs()
        data.update(weapons)
        async with aiofiles.open(ASSETS_GS_PATH, "w", encoding="utf-8") as f:
            await f.write(ujson.dumps(data, ensure_ascii=False, indent=4))

    # MC
    @staticmethod
    def get_icon_url_mc(path: str) -> str:
        new_path = path.replace("Game/Aki", "ww")
        ext = new_path.split(".")[-1]
        if ext != "webp":
            ext_index = new_path.rfind(ext)
            new_path = new_path[:ext_index] + "webp"
        return f"https://api.hakush.in{new_path}"

    async def fetch_avatars_mc(self):
        data = await self.fetch("https://api.hakush.in/ww/data/character.json")
        new_data = {}
        for item in data.values():
            new_data[item["zh-Hans"]] = self.get_icon_url_mc(item["icon"])
        return new_data

    async def fetch_weapons_mc(self):
        data = await self.fetch("https://api.hakush.in/ww/data/weapon.json")
        new_data = {}
        for item in data.values():
            new_data[item["zh-Hans"]] = self.get_icon_url_mc(item["icon"])
        return new_data

    async def main_mc(self):
        data = {}
        avatars = await self.fetch_avatars_mc()
        data.update(avatars)
        weapons = await self.fetch_weapons_mc()
        data.update(weapons)
        async with aiofiles.open(ASSETS_MC_PATH, "w", encoding="utf-8") as f:
            await f.write(ujson.dumps(data, ensure_ascii=False, indent=4))

    async def main(self):
        await self.main_gs()
        await self.main_mc()


if __name__ == "__main__":
    import asyncio

    gen = AssetsGen()
    asyncio.run(gen.main())
