from __future__ import annotations

from enum import StrEnum


class Game(StrEnum):
    GENSHIN = "genshin"
    STARRAIL = "hsr"
    ZZZ = "zzz"
    MC = "mc"


BANNER_TYPE_NAMES = {
    Game.GENSHIN: ["角色祈愿", "武器祈愿", "常驻祈愿", "新手祈愿", "集录祈愿"],
    Game.STARRAIL: ["角色跃迁", "光锥跃迁", "常驻跃迁", "新手跃迁"],
    Game.ZZZ: ["代理人调频", "音擎调频", "常驻调频", "邦布调频"],
    Game.MC: ["角色祈愿", "武器祈愿", "常驻祈愿", "常驻武器祈愿", "新手祈愿"],
}
