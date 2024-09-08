from __future__ import annotations

import flet as ft


class LoadingSnackBar(ft.SnackBar):
    def __init__(
        self,
        *,
        message: str | None = None,
    ) -> None:
        text = message or "Loading..."

        super().__init__(
            content=ft.Row(
                [
                    ft.ProgressRing(
                        width=16,
                        height=16,
                        stroke_width=2,
                        color=ft.colors.ON_SECONDARY_CONTAINER,
                    ),
                    ft.Text(text, color=ft.colors.ON_SECONDARY_CONTAINER),
                ]
            ),
            bgcolor=ft.colors.SECONDARY_CONTAINER,
        )


class ErrorBanner(ft.Banner):
    def __init__(self, message: str) -> None:
        super().__init__(
            leading=ft.Icon(ft.icons.ERROR, color=ft.colors.ON_ERROR_CONTAINER),
            content=ft.Text(message, color=ft.colors.ON_ERROR_CONTAINER),
            bgcolor=ft.colors.ERROR_CONTAINER,
            actions=[
                ft.IconButton(
                    ft.icons.CLOSE,
                    on_click=self.on_action_click,
                    icon_color=ft.colors.ON_ERROR_CONTAINER,
                )
            ],
        )

    async def on_action_click(self, e: ft.ControlEvent) -> None:
        page: ft.Page = e.page
        await page.close_banner_async()


async def show_loading_snack_bar(
    page: ft.Page,
    *,
    message: str | None = None,
) -> None:
    await page.show_snack_bar_async(
        LoadingSnackBar(message=message),
    )


async def show_error_banner(page: ft.Page, *, message: str) -> None:
    await page.show_banner_async(ErrorBanner(message))
