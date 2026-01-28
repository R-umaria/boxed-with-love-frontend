import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SESSION_COOKIE_NAME = "boxedwithlove_session"
