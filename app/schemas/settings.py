from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
import os
env_path = find_dotenv()
load_dotenv(env_path)  # take environment variables from .env.


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('JWT')
