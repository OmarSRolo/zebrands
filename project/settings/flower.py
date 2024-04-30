from decouple import config

username: str = config("FLOWER_USER", default="")
user_password: str = config("FLOWER_PASSWORD", default="")
basic_auth: list[str] = [f"{username}:{user_password}"]
