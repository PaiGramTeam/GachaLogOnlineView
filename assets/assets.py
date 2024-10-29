import ujson

from assets.gen import ASSETS_GS_PATH, ASSETS_MC_PATH
from web_app.enums import Game


DEFAULT_ICON = "favicon.png"


class Assets:
    def __init__(self):
        self.genshin_assets = {}
        self.mc_assets = {}
        self.load()

    def load(self):
        with open(ASSETS_GS_PATH, "r", encoding="utf-8") as f:
            self.genshin_assets = ujson.load(f)
        with open(ASSETS_MC_PATH, "r", encoding="utf-8") as f:
            self.mc_assets = ujson.load(f)

    def get_gacha_icon_genshin(self, item_id: str) -> str:
        return self.genshin_assets.get(item_id, DEFAULT_ICON)

    def get_gacha_icon_mc(self, item_id: str) -> str:
        return self.mc_assets.get(item_id, DEFAULT_ICON)

    @staticmethod
    def get_gacha_icon_starrail(item_id: str) -> str:
        if len(str(item_id)) == 5:  # light cone
            return f"https://stardb.gg/api/static/StarRailResWebp/icon/light_cone/{item_id}.webp"
        # character
        return f"https://stardb.gg/api/static/StarRailResWebp/icon/character/{item_id}.webp"

    def get_gacha_icon(self, game: Game, item_id: str) -> str:
        if game is Game.GENSHIN:
            return self.get_gacha_icon_genshin(item_id)
        elif game is Game.STARRAIL:
            return self.get_gacha_icon_starrail(item_id)
        elif game is Game.ZZZ:
            return f"https://stardb.gg/api/static/zzz/{item_id}.png"
        elif game is Game.MC:
            return self.get_gacha_icon_mc(item_id)
        return DEFAULT_ICON

    def get_hash(self) -> str:
        return self.genshin_assets["hash"] + self.mc_assets["hash"]


assets = Assets()
