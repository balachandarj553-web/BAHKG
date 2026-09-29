from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    debug: bool = True

    gemini_api_key: str = ""

    gemini_flash_model: str = "gemini-3.8-flash"
    gemini_pro_model: str = "gemini-3.8-flash"
    gemini_image_model: str = "gemini-3.1-flash-image"

    hf_token: str = ""
    hf_provider: str = "auto"
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"

    static_dir: Path = BASE_DIR / "static"
    panels_dir: Path = BASE_DIR / "static" / "panels"
    exports_dir: Path = BASE_DIR / "static" / "exports"
    templates_dir: Path = BASE_DIR / "templates"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def ai_enabled(self) -> bool:
        return bool(self.gemini_api_key)


settings = Settings()


for directory in (
    settings.static_dir,
    settings.panels_dir,
    settings.exports_dir,
    settings.templates_dir,
):
    directory.mkdir(parents=True, exist_ok=True)