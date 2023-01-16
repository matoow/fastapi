from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My fastapi app"
    admin_email: str = "matoow@gmail.com"
    items_per_user: int = 50
    gh_client_id: str = "Iv1.5977bf5d625594cd"
    gh_client_secret: str = "e0505bfcd8553630377f4eedfe9b8a0a908bdc1e"
    gh_callback_url: str = "http://localhost:8000/auth/github/callback"


settings = Settings()
