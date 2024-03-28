from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False, env_prefix='DB_')
    user: str
    port: int
    host: str
    password: str
    db: str
    uri: str
    token: str
    provider_token : str
    top_up : int
    
    @property
    def get_url(self) -> str:
        return self.uri.format(self.user, self.password, self.host, self.port, self.db)

def load_setting() -> Setting:
    return Setting()
