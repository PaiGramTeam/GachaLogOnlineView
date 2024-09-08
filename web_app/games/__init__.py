from .base import BaseGachaLogInfo, BaseGachaItem, BaseGachaLogFunctions
from .genshin import genshin_gacha_log_functions
from .starrail import starrail_gacha_log_functions
from .zzz import zzz_gacha_log_functions
from .mc import mc_gacha_log_functions

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from web_app.enums import Game


__all__ = [
    "BaseGachaLogInfo",
    "BaseGachaItem",
    "genshin_gacha_log_functions",
    "starrail_gacha_log_functions",
    "zzz_gacha_log_functions",
    "mc_gacha_log_functions",
]


def get_gacha_log_functions(game: "Game") -> BaseGachaLogFunctions:
    from web_app.enums import Game

    if game is Game.GENSHIN:
        return genshin_gacha_log_functions
    if game is Game.STARRAIL:
        return starrail_gacha_log_functions
    if game is Game.ZZZ:
        return zzz_gacha_log_functions
    return mc_gacha_log_functions
