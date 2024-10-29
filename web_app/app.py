from __future__ import annotations

import asyncio
import urllib.parse
from typing import TYPE_CHECKING, Any

import flet as ft

from assets.assets import assets
from fast_app.functions.pb import PBFunctions
from . import pages
from .enums import Game
from .games import get_gacha_log_functions, BaseGachaItem
from .schema import GachaParams

if TYPE_CHECKING:
    from collections.abc import Sequence


class WebApp:
    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._page.on_route_change = self.on_route_change

    async def initialize(self) -> None:
        self._page.theme_mode = ft.ThemeMode.DARK
        await self._page.go_async(self._page.route)

    async def on_route_change(self, e: ft.RouteChangeEvent) -> Any:
        page: ft.Page = e.page
        parsed = urllib.parse.urlparse(e.route)
        route = parsed.path

        parsed_params = {
            k: v[0] for k, v in urllib.parse.parse_qs(parsed.query).items()
        }

        view = None
        if "gacha" in route:
            view = await self._handle_gacha_routes(route, parsed_params)
            page.title = "抽卡记录在线查询"
            if view is not None:
                view.appbar = self.gacha_app_bar

        if view is None:
            return

        view.scroll = ft.ScrollMode.AUTO

        page.views.clear()
        page.views.append(view)
        await page.update_async()

    async def _handle_gacha_routes(
        self, route: str, parsed_params: dict[str, str]
    ) -> ft.View | None:
        page = self._page

        try:
            params = GachaParams(**parsed_params)
            game, uid = await PBFunctions.get_uid_by_hash(params.account_id)
            gacha_log_functions = get_gacha_log_functions(game)
            params.uid = uid
        except ValueError:
            return pages.ErrorPage(code=422, message="Invalid parameters")
        except FileNotFoundError:
            return pages.ErrorPage(code=404, message="已失效，请尝试重新获取")

        if route == "/gacha_log":
            filtered_logs = await gacha_log_functions.get_gacha_logs_base(params)
            total_row = len(filtered_logs)
            gacha_logs = filtered_logs[
                (params.page - 1) * params.size : params.page * params.size
            ]
            gacha_icons, gacha_icons_hash = await self._get_gacha_icons(game, gacha_logs)
            await asyncio.create_task(
                page.client_storage.set_async("gacha_log.gacha_icons", gacha_icons)
            )
            await asyncio.create_task(
                page.client_storage.set_async("gacha_log.gacha_icons_hash", gacha_icons_hash)
            )

            view = pages.GachaLogPage(
                gacha_histories=gacha_logs,
                gacha_icons=gacha_icons,
                game=game,
                params=params,
                max_page=(total_row + params.size - 1) // params.size,
            )
        else:
            view = pages.ErrorPage(code=404, message="Not Found")

        return view

    async def _get_gacha_icons(
        self, game: Game, gachas: Sequence[BaseGachaItem]
    ) -> tuple[dict[str | int, str], str]:
        gacha_icons_hash = assets.get_hash()
        cached_gacha_icons_hash: str = await self._page.client_storage.get_async("gacha_log.gacha_icons_hash") or ""
        if gacha_icons_hash == cached_gacha_icons_hash:
            cached_gacha_icons: dict[str | int, str] = (
                    await self._page.client_storage.get_async("gacha_log.gacha_icons") or {}
            )
        else:
            cached_gacha_icons = {}
        result: dict[str | int, str] = {}
        for gacha in gachas:
            key = gacha.key
            if key in cached_gacha_icons:
                result[key] = cached_gacha_icons[key]
            else:
                result[key] = assets.get_gacha_icon(game=game, item_id=key)
                cached_gacha_icons[key] = result[key]

        await asyncio.create_task(
            self._page.client_storage.set_async(
                "gacha_log.gacha_icons", cached_gacha_icons
            )
        )
        await asyncio.create_task(
            self._page.client_storage.set_async(
                "gacha_log.gacha_icons_hash", gacha_icons_hash
            )
        )
        return result, gacha_icons_hash

    @property
    def gacha_app_bar(self) -> ft.AppBar:
        return ft.AppBar(
            title=ft.Row(
                [
                    ft.Image(src="/images/logo.png", width=32, height=32),
                    ft.Container(
                        ft.Text("抽卡记录在线查询"), margin=ft.margin.only(left=4)
                    ),
                ]
            ),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(
                    ft.icons.QUESTION_MARK, url="https://t.me/PaiGramTeamChat"
                )
            ],
        )
