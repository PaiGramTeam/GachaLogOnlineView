from typing import Dict, List

import ujson

from web_app.enums import Game
from web_app.games.base import BaseGachaLogFunctions

from .base import BaseGachaItem, BaseGachaLogInfo


class GachaItem(BaseGachaItem):
    gacha_id: str = ""
    item_id: str = ""

    @property
    def key(self) -> str:
        return self.item_id or self.name


class GachaLogInfo(BaseGachaLogInfo):
    item_list: Dict[str, List[GachaItem]] = {
        "代理人调频": [],
        "音擎调频": [],
        "常驻调频": [],
        "邦布调频": [],
    }


class ZZZGachaLogFunctions(BaseGachaLogFunctions):
    def __init__(self):
        super().__init__()
        self.gacha_log_path = self.BASE_DATA_PATH / Game.ZZZ.value

    async def load_history_info(self, uid: int) -> GachaLogInfo:
        """读取历史抽卡记录数据
        :param uid: 原神uid
        :return: 抽卡记录数据
        """
        file_path = self.gacha_log_path / f"{uid}.json"
        if not file_path.exists():
            raise FileNotFoundError
        try:
            return GachaLogInfo.model_validate(await self.load_json(file_path))
        except ujson.JSONDecodeError:
            raise FileNotFoundError

    async def get_history_info(self, uid: int) -> GachaLogInfo:
        return await self.get_history_info_base(uid)


zzz_gacha_log_functions = ZZZGachaLogFunctions()
