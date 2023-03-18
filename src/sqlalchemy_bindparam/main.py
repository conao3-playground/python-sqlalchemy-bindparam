import logging
import logging.config
from typing import Any

import pydantic
import psycopg2.extras
import psycopg2.extensions
import sqlparse
import yaml
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm


### logging

with open('logging.conf.yml', 'r') as f:
    logging.config.dictConfig(yaml.safe_load(f))

logger = logging.getLogger(__name__)
logger_db = logging.getLogger(f'{__name__}/db')


### load settings from .env file

class Settings(pydantic.BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    class Config:  # type: ignore
        env_file = ".env"


settings = Settings()  # type: ignore


### database connection

class LoggingConnection(psycopg2.extras.LoggingConnection):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)
        self.initialize(logger_db)

    def _logtologger(self, msg: str | bytes, cur: psycopg2.extensions.cursor):
        msg = self.filter(msg, cur)
        if msg:
            if isinstance(msg, bytes):
                msg = msg.decode("utf-8")
                msg = sqlparse.format(msg, reindent=True, keyword_case="upper")

            self._logobj.info(msg)  # type: ignore


engine = sa.create_engine(
    f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}",
    connect_args={'connection_factory': LoggingConnection},
)
session = sa_orm.scoped_session(
    sa_orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


class Base(sa_orm.DeclarativeBase):
    query = session.query_property()

    def __repr__(self) -> str:
        args = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return f'{self.__class__.__name__}({args})'


class User(Base):
    __tablename__ = "user"

    user_cd = sa.Column(sa.String, primary_key=True)


def main1():
    logger.info("Hello World!")
    logger.info(settings)
    logger.info(User.query.all())


def main2():
    logger.info(User.query.filter(User.user_cd == 'u-001').one())


if __name__ == "__main__":
    main2()
