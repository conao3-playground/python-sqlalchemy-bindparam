import pydantic


### load settings from .env file

class Settings(pydantic.BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_port: int

    class Config:  # type: ignore
        env_file = ".env"


settings = Settings()  # type: ignore


def main1():
    print("Hello World!")
    print(settings)


main1()
