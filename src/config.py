import os
from pathlib import Path
from typing import Self
from dotenv import load_dotenv


class Gateway:
    def __init__(self: Self):
        self.VALHALLA_HOST = os.getenv('VALHALLA_HOST')
        self.VALHALLA_PORT = os.getenv('VALHALLA_PORT')
        self.overpass_request_url = "http://overpass-api.de/api/interpreter"
        

    def nominatim_request_url(self: Self, address: str) -> str:
        return f'https://nominatim.openstreetmap.org/search?q={address}&format=json'

    @property
    def valhalla_request_url(self: Self):
        return (
            f"http://{self.VALHALLA_HOST}:{self.VALHALLA_PORT}/route"
        )
     
  

class Db:
    def __init__(self: Self):
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_PASS = os.getenv('DB_PASS')
        self.DB_PORT = os.getenv('DB_PORT')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_NAME = os.getenv('DB_NAME')


    @property
    def dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class Redis:
    def __init__(self: Self):
        self.REDIS_HOST = os.getenv('REDIS_HOST') 
        self.REDIS_PORT = os.getenv('REDIS_PORT')


    @property
    def dsn(self) -> str:
        return (
            f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
        )


class SetupSettings:
    def __init__(self: Self):
        self.non_stop_drive_limit = 25200
        


class Settings:
    def __init__(self: Self, env_file: str):
        env_path = f'{Path(__file__).resolve().parents[1]}/{env_file}'
        load_dotenv(env_path, override=True)

        self.SECRET = os.getenv('SECRET')
        self.APP_PORT = os.getenv('APP_PORT')
        self.APP_DOMAIN = os.getenv('APP_DOMAIN')
        self.MODE = os.getenv('MODE')

        self.db = Db()
        self.redis = Redis()
        self.gateway = Gateway()

        self.setup = SetupSettings()




settings = Settings('.env')