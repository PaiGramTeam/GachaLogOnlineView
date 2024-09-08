from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import flet as ft

from web_app.enums import Game, BANNER_TYPE_NAMES
from web_app.games import BaseGachaItem
from web_app.schema import GachaParams
from web_app.utils import show_error_banner

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = ("GachaLogPage",)


class GachaLogPage(ft.View):
    def __init__(
        self,
        *,
        gacha_histories: Sequence[BaseGachaItem],
        gacha_icons: dict[str | int, str],
        params: GachaParams,
        game: Game,
        max_page: int,
    ) -> None:
        self.game = game
        self.gachas = gacha_histories
        self.gacha_icons = gacha_icons
        self.params = params
        self.max_page = max_page

        super().__init__(
            controls=[
                ft.SafeArea(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.TextField(
                                        label="搜索",
                                        prefix_icon=ft.icons.SEARCH,
                                        on_submit=self.on_search_bar_submit,
                                        value=params.name_contains,
                                    ),
                                    ft.OutlinedButton(
                                        text="筛选条件",
                                        icon=ft.icons.FILTER_ALT,
                                        on_click=self.filter_button_on_click,
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.ARROW_BACK_IOS,
                                        on_click=self.previous_page_on_click,
                                        disabled=params.page == 1,
                                    ),
                                    ft.TextField(
                                        label="页数",
                                        value=str(params.page),
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        on_submit=self.page_field_on_submit,
                                        width=80,
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.ARROW_FORWARD_IOS,
                                        on_click=self.next_page_on_click,
                                        disabled=params.page == max_page,
                                    ),
                                ],
                                wrap=True,
                            ),
                            ft.GridView(
                                self.gacha_log_controls,
                                expand=1,
                                runs_count=5,
                                max_extent=100,
                                child_aspect_ratio=1.0,
                                spacing=16,
                                run_spacing=16,
                            ),
                        ]
                    ),
                    minimum_padding=8,
                )
            ]
        )

    @property
    def gacha_log_controls(self) -> list[ft.Container]:
        rarity_colors: dict[int, str] = {3: "#3e4857", 4: "#4d3e66", 5: "#915537"}
        paddings: dict[Game, int] = {
            Game.GENSHIN: 0,
            Game.ZZZ: 8,
            Game.STARRAIL: 0,
            Game.MC: 0,
        }
        result: list[ft.Container] = []

        for gacha in self.gachas:
            key = gacha.key
            stack_controls = [
                ft.Container(
                    ft.Image(src=self.gacha_icons[key], border_radius=8),
                    padding=ft.padding.all(paddings[self.game]),
                ),
            ]
            result.append(
                ft.Container(
                    ft.Stack(stack_controls),
                    bgcolor=rarity_colors[gacha.rank_type],
                    border_radius=8,
                    on_click=self.container_on_click,
                    data=gacha.id,
                )
            )

        return result

    async def container_on_click(self, e: ft.ControlEvent) -> None:
        page: ft.Page = e.page
        gacha = next(g for g in self.gachas if g.id == e.control.data)

        await page.show_dialog_async(
            GachaLogDialog(
                gacha=gacha,
            )
        )

    async def filter_button_on_click(self, e: ft.ControlEvent) -> None:
        page: ft.Page = e.page
        await page.show_dialog_async(
            FilterDialog(
                params=self.params,
                game=self.game,
            )
        )

    async def on_search_bar_submit(self, e: ft.ControlEvent) -> None:
        page: ft.Page = e.page
        self.params.name_contains = e.control.value.lower()
        self.params.page = 1
        await page.go_async(f"/gacha_log?{self.params.to_query_string()}")

    async def next_page_on_click(self, e: ft.ControlEvent) -> None:
        page: ft.Page = e.page
        self.params.page += 1
        await page.go_async(f"/gacha_log?{self.params.to_query_string()}")

    async def previous_page_on_click(self, e: ft.ControlEvent) -> None:
        page: ft.Page = e.page
        self.params.page -= 1
        await page.go_async(f"/gacha_log?{self.params.to_query_string()}")

    async def page_field_on_submit(self, e: ft.ControlEvent) -> None:
        page: ft.Page = e.page
        page_num = int(e.control.value)
        if page_num < 1 or page_num > self.max_page:
            await show_error_banner(page, message="Invalid page number")
            return

        self.params.page = page_num
        await page.go_async(f"/gacha_log?{self.params.to_query_string()}")


class GachaLogDialog(ft.AlertDialog):
    def __init__(
        self,
        *,
        gacha: BaseGachaItem,
    ) -> None:
        gacha_time = gacha.time.astimezone(
            datetime.timezone(datetime.timedelta(hours=8))
        )
        time_string = gacha_time.strftime("%Y-%m-%d %H:%M:%S") + " UTC+8"

        text = f"ID: {gacha.id}\n名称: {gacha.name}\n抽取时间: {time_string}"
        super().__init__(
            content=ft.Text(text),
            title=ft.Text("抽卡物品详情"),
            actions=[
                ft.TextButton(
                    text="关闭",
                    on_click=self.close_dialog,
                )
            ],
        )

    async def close_dialog(self, e: ft.ControlEvent) -> None:
        await e.page.close_dialog_async()


class FilterDialog(ft.AlertDialog):
    def __init__(self, *, params: GachaParams, game: Game) -> None:
        self.params = params
        self.game = game

        super().__init__(
            title=ft.Text("抽卡纪录筛选条件"),
            actions=[
                ft.TextButton(
                    text="取消",
                    on_click=self.on_dialog_cancel,
                ),
                ft.TextButton(
                    text="完成",
                    on_click=self.on_dialog_close,
                ),
            ],
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Checkbox(
                                label=f"{rarity} ★",
                                value=rarity in params.rarities,
                                data=rarity,
                                on_change=self.on_rarity_checkbox_change,
                            )
                            for rarity in (3, 4, 5)
                        ]
                    ),
                    ft.Dropdown(
                        options=[
                            ft.dropdown.Option(
                                text=banner_type,
                                data=str(banner_type),
                            )
                            for banner_type in BANNER_TYPE_NAMES[game]
                        ],
                        value=params.banner_type,
                        on_change=self.on_banner_type_dropdown_change,
                    ),
                    ft.TextField(
                        label="每页物品数",
                        value=str(params.size),
                        on_change=self.on_size_text_field_change,
                    ),
                ],
                tight=True,
            ),
        )

    async def on_banner_type_dropdown_change(self, e: ft.ControlEvent) -> None:
        self.params.banner_type = e.control.value

    async def on_rarity_checkbox_change(self, e: ft.ControlEvent) -> None:
        rarity = e.control.data
        if rarity in self.params.rarities:
            self.params.rarities.remove(rarity)
        else:
            self.params.rarities.append(rarity)

    async def on_size_text_field_change(self, e: ft.ControlEvent) -> None:
        size = int(e.control.value)
        self.params.size = min(max(size, 1), 500)

    async def on_dialog_close(self, e: ft.ControlEvent) -> None:
        page: ft.Page = e.page
        await page.close_dialog_async()
        self.params.page = 1
        await page.go_async(f"/gacha_log?{self.params.to_query_string()}")

    async def on_dialog_cancel(self, e: ft.ControlEvent) -> None:
        page: ft.Page = e.page
        await page.close_dialog_async()
