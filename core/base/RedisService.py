"""
    Service class to work with Redis Server
"""

import json

import redis
from django.conf import settings

from core.misc.Nomenclature import Nomenclature


class RedisService:
    prefix: str = settings.PREFIX
    """
    Service to work with Redis Server
    """

    def __init__(self, tenant: str):
        assert tenant is not None
        self.tenant = f"{tenant}_{self.prefix}"
        self.redis = redis.StrictRedis.from_url(url=settings.REDIS_SERVER)

    def generate_serial(self, serial_nm: str):
        serial_code: str = "serial_" + serial_nm
        previous_serial: dict = self.get_item(serial_code)
        next_count: int = 1
        if previous_serial:
            next_count: int = previous_serial["count"] * 1 + 1
        next_serial: str = Nomenclature.set_serial(serial_nm, next_count)
        self.set_item(serial_code, {serial_code: next_serial, "count": next_count})
        return next_serial

    def set_item(self, key, value):
        """
        Insert a value in the server
        :param key: Key where it is going to save
        :param value: Value to save
        """
        key: str = f'{self.tenant}_{key}'
        value: str = json.dumps(value)
        self.redis.set(key, value)

    def get_item(self, key, out_format="dict"):
        """
        Get a value from the server
        :param key: Key where it is going to get the value
        :param out_format: Specific format to get the data
        :return The value
        """
        key: str = f'{self.tenant}_{key}'
        item: str = self.redis.get(key)
        if item:
            if out_format == "dict":
                return dict(json.loads(item))
            if out_format == "json":
                return json.loads(item)
        return item


class OrchestratorRedisService:

    def __init__(self):
        self.redis = None
        self.is_configured = False
        if settings.USE_REDIS:
            url = settings.REDIS_SERVER
            self.redis = redis.StrictRedis.from_url(url=url)
            self.is_configured = True

    def get_lock(self, key, lock_timeout=1) -> bool:
        if self.is_configured:
            try:
                res = self.redis.set(name=key, value=0, ex=lock_timeout, nx=True)
                return res
            except Exception as e:
                print(e)
                return False
        else:
            return True

    def release_lock(self, key):
        if self.is_configured:
            return self.redis.expire(key, 0)
