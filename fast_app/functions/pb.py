import aiofiles
import os
from cashews import cache
from fastapi import UploadFile
from pathlib import Path

from web_app.enums import Game

DATA_PATH = Path("data") / "gacha_log"
DATA_PATH.mkdir(exist_ok=True, parents=True)


class PBFunctions:
    @staticmethod
    async def save_file(file: UploadFile, uid: int, game: Game) -> None:
        file_path = DATA_PATH / f"{game.value}" / f"{uid}.json"
        file_path.parent.mkdir(exist_ok=True, parents=True)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(await file.read())

    @staticmethod
    async def create_hash(uid: int, game: Game) -> str:
        hash_str = os.urandom(16).hex()
        await cache.set(hash_str, f"{game.value}_{uid}")
        return hash_str

    @staticmethod
    async def get_uid_by_hash(hash_str: str) -> tuple[Game, int]:
        uid_str = await cache.get(hash_str)
        if not uid_str:
            raise FileNotFoundError
        game, uid = uid_str.split("_")
        return Game(game), int(uid)
