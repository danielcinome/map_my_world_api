import os
from dotenv import load_dotenv

load_dotenv()


class EnvManager:
    SQLALCHEMY_DATABASE_URL: str = os.environ.get('SQLALCHEMY_DATABASE_URL')
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    ALGORITHM: str = os.environ.get('ALGORITHM')
    TESTING_DB_URL: str = os.environ.get('TESTING_DB_URL', 'sqlite:///./test.db?check_same_thread=False')