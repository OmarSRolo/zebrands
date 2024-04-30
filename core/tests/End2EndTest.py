import base64
import json
import random

from core.tests.BaseTest import BaseTest
from core.tests.UtilsFixtures import UtilFixture
from core.tests import Benchmark


class End2EndTest(UtilFixture, BaseTest):

    def assert_elapsed_time(self, bench_mark: Benchmark, time_limit: int = 3000):
        self.assertLessEqual(bench_mark.elapsed, time_limit, f"Elapsed time grater than {time_limit} ms")

    def assert_compare_data(self, item_data, response_data, attrs, msg=""):
        item_data, response_data = json.dumps(item_data), json.dumps(response_data)
        for attr in attrs:
            self.assertEqual(item_data[attr], response_data[attr], f"The {attr} is not equals.")

    def assert_response(self, response, msg="", expected_status_code=200):
        if msg:
            msg = f" ({msg})"
        self.assertEqual(response.status_code, expected_status_code, f"The response is not same status code." + msg)

    def get_random_item(self, items):
        count = len(items)
        self.assertGreater(count, 0, f"There are no items to select.")
        return items[random.randint(0, count - 1)]

    @staticmethod
    def encode_data(data) -> str:
        return base64.b64encode(json.dumps(data).encode('ascii')).decode('ascii')

    @staticmethod
    def count_items_per_page(limit: int, offset: int, total: int) -> int:
        accumulate = 0
        for i in range(offset + 1):
            accumulate += limit
            if accumulate >= total:
                break
        return limit if accumulate <= total else limit - (accumulate - total)
