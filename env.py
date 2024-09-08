import dotenv
from pydantic.v1 import BaseSettings

dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv(usecwd=True))


class Settings(BaseSettings):
    def __new__(cls, *args, **kwargs):
        cls.update_forward_refs()
        return super(Settings, cls).__new__(cls)  # pylint: disable=E1120

    class Config(BaseSettings.Config):
        case_sensitive = False


class PBConfig(Settings):
    token: str = ""
    """pb token for upload"""

    class Config(Settings.Config):
        env_prefix = "pb_"


class WebConfig(Settings):
    host: str = "0.0.0.0"
    port: int = 5688

    class Config(Settings.Config):
        env_prefix = "web_"


class ApplicationConfig(Settings):
    pb: PBConfig = PBConfig()
    web: WebConfig = WebConfig()


ApplicationConfig.update_forward_refs()
config = ApplicationConfig()
