import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


@dataclass
class BotConfig:
    token: str = os.getenv("TG_BOT_TOKEN")


@dataclass
class DBConfig:
    name: str = os.getenv("DB_NAME")
    user: str = os.getenv("DB_USERNAME")
    passwd: str = os.getenv("DB_PASSWORD")
    port: int = int(os.getenv("DB_PORT"))
    host: str = os.getenv("DB_HOST")

    driver: str = os.getenv("DRIVER")
    database_system: str = os.getenv("DATABASE_SYSTEM")

    @property
    def build_connection_str(self) -> str:
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class RedisConfig:
    db: int = int(os.getenv("REDIS_DATABASE", 1))
    host: str = os.getenv("REDIS_HOST", "redis")
    port: int = int(os.getenv("REDIS_PORT", 6379))
    passwd: str | None = os.getenv("REDIS_PASSWORD")
    username: str | None = os.getenv("REDIS_USERNAME")
    state_ttl: int | None = os.getenv("REDIS_TTL_STATE", None)
    data_ttl: int | None = os.getenv("REDIS_TTL_DATA", None)


@dataclass
class PathsConfig:
    root_path: str = str(Path(__file__).parent.parent)

    log_dir_name: str = os.getenv("LOG_DIR_NAME")
    info_log_file_name: str = os.getenv("INFO_LOG_FILE_NAME")
    debug_log_file_name: str = os.getenv("DEBUG_LOG_FILE_NAME")

    images_dir_name: str = os.getenv("IMAGES_DIR_NAME")
    start_image_name: str = os.getenv("START_IMAGE_NAME")
    calc_image_name: str = os.getenv("CALC_IMAGE_NAME")

    templates_dir_name: str = os.getenv("TEMPLATES_DIR_NAME")
    products_template_name: str = os.getenv("PRODUCTS_TEMPLATE_FILE_NAME")

    @property
    def products_template_path(self) -> str:
        return os.path.join(self.root_path, self.templates_dir_name, self.products_template_name)

    @property
    def info_log_path(self) -> str:
        return os.path.join(self.root_path, self.log_dir_name, self.info_log_file_name)

    @property
    def debug_log_path(self) -> str:
        return os.path.join(self.root_path, self.log_dir_name, self.debug_log_file_name)

    @property
    def start_image_path(self) -> str:
        return os.path.join(self.root_path, self.images_dir_name, self.start_image_name)

    @property
    def calc_image_path(self) -> str:
        return os.path.join(self.root_path, self.images_dir_name, self.calc_image_name)


@dataclass
class Config:
    log_level: str = os.getenv("LOG_LEVEL")
    admins: list[int] = field(
        default_factory=lambda: list(map(int, os.getenv("ADMINS").split(",")))
    )
    manager_username: str = os.getenv("MANAGER_USERNAME")

    time_format = os.getenv("TIME_FORMAT")

    bot: BotConfig = field(default_factory=BotConfig)
    db: DBConfig = field(default_factory=DBConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)


cfg = Config()
