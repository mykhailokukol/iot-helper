from pathlib import Path


class Settings:
    BASE_DIR: str = Path(__file__).resolve().parent.parent
    

settings = Settings()