import flet.fastapi as flet_fastapi
from cashews import cache
from pathlib import Path
from logging import basicConfig, INFO

from env import config
from fast_app.app import app
from web_app.main import web_app_entry

basicConfig(level=INFO)
cache.setup("mem://")
ASSETS_PATH = Path(__file__).parent / "web_app" / "assets"
app.mount(
    "/",
    flet_fastapi.app(
        web_app_entry,
        assets_dir=str(ASSETS_PATH),
        use_color_emoji=True,
    ),
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.web.host, port=config.web.port)
