from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="BOT__",
    )

    bot_token: str
    webhook_secret_token: str = ""
    admin_ids: frozenset[int] = frozenset({42, 3595399})


# noinspection PyArgumentList
settings = Settings()
