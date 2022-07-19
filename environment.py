from typing import Optional

from yarl import URL

from pydantic import BaseSettings, validator


class UrlSettings(BaseSettings):
    stage: str

    class Config:
        env_prefix = "TEST_"


class StageSettings(UrlSettings):
    dev: URL = URL("https://playground.learnqa.ru/api_dev/")
    prod: URL = URL("https://playground.learnqa.ru/api/")

    @validator("dev", "prod")
    def make_url(cls, v: Optional[str]) -> Optional[URL]:
        if isinstance(v, str):
            return URL(v)
        return v

    @property
    def connection_url(self) -> URL:
        if self.stage == "dev":
            return self.dev
        if self.stage == "prod":
            return self.prod
        raise BaseException("ойойой пердали в env TEST_STAGE какую то ерунду")
