import asyncio
import datetime
from abc import abstractmethod
from pathlib import Path
from typing import Any, TYPE_CHECKING, List

import aiofiles
import pytz
import ujson as json
from pydantic import BaseModel

from fast_app.scheduler import scheduler

if TYPE_CHECKING:
    from web_app.schema import GachaParams


class BaseGachaItem(BaseModel):
    id: str
    name: str
    gacha_type: str
    item_type: str
    rank_type: int
    time: datetime.datetime

    @property
    def key(self) -> str:
        return self.name


class BaseGachaLogInfo(BaseModel):
    user_id: str
    uid: str
    update_time: datetime.datetime


class BaseGachaLogFunctions:
    BASE_DATA_PATH = Path("data") / "gacha_log"
    DATA_MAP: dict[int, Any]
    DATA_MAP_LOCK: asyncio.Lock

    def __init__(self):
        self.BASE_DATA_PATH.mkdir(exist_ok=True, parents=True)
        self.DATA_MAP = {}
        self.DATA_MAP_LOCK = asyncio.Lock()

    @staticmethod
    async def load_json(path):
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            return json.loads(await f.read())

    @abstractmethod
    async def load_history_info(self, uid: int):
        pass

    @abstractmethod
    async def get_history_info(self, uid: int):
        pass

    async def get_history_info_base(self, uid: int):
        async with self.DATA_MAP_LOCK:
            if uid not in self.DATA_MAP:
                self.DATA_MAP[uid] = await self.load_history_info(uid)
                # 1小时后删除缓存
                scheduler.add_job(
                    self.remove_history_info_from_map,
                    "date",
                    id=f"remove_history_info_from_map_{uid}",
                    name=f"remove_history_info_from_map_{uid}",
                    run_date=datetime.datetime.now(pytz.timezone("Asia/Shanghai"))
                    + datetime.timedelta(seconds=3600),
                    replace_existing=True,
                    args=(uid,),
                )
            return self.DATA_MAP[uid]

    async def remove_history_info_from_map(self, uid: int):
        async with self.DATA_MAP_LOCK:
            if uid in self.DATA_MAP:
                del self.DATA_MAP[uid]

    async def get_gacha_logs_base(self, params: "GachaParams") -> List[BaseGachaItem]:
        history_info = await self.get_history_info(params.uid)
        items = history_info.item_list.get(params.banner_type)
        if not items:
            return []
        data = []
        for i in items[::-1]:
            if params.rarities and i.rank_type not in params.rarities:
                continue
            if params.name_contains and params.name_contains not in i.name:
                continue
            data.append(i)
        return data
