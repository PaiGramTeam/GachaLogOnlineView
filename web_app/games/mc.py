from typing import Dict, List

import ujson

from web_app.enums import Game
from web_app.games.base import BaseGachaLogFunctions

from .base import BaseGachaItem, BaseGachaLogInfo


class GachaItem(BaseGachaItem):
    """"""


class GachaLogInfo(BaseGachaLogInfo):
    item_list: Dict[str, List[GachaItem]] = {
        "角色祈愿": [],
        "武器祈愿": [],
        "常驻祈愿": [],
        "常驻武器祈愿": [],
        "新手祈愿": [],
    }


class MCGachaLogFunctions(BaseGachaLogFunctions):
    def __init__(self):
        super().__init__()
        self.gacha_log_path = self.BASE_DATA_PATH / Game.MC.value

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


mc_gacha_log_functions = MCGachaLogFunctions()
