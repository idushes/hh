from pydantic import BaseSettings, Field


class Config(BaseSettings):
    base_url: str = "https://api.hh.ru"
    token: str = Field(env='HH_TOKEN')
    test_offline = False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def hh_headers(self):
        return {
            "HH-User-Agent": "LISA HR/1.0 (admin@lisacorp.com)",
            "Authorization": "Bearer " + self.token
        }
