"""
    news_unit_tests.py
    This file does all tests for news.py
"""
import sys
import unittest
import unittest.mock as mock
import datetime
from os.path import dirname, join
# pylint: disable=C0413
sys.path.append(join(dirname(__file__), "../"))
import bills


# pylint: disable=W0613
class BillsTestCases(unittest.TestCase):
    """Make all the test cases"""

    # pylint: disable=R0201
    def mock_json_load_nocache(self, file):
        """Mock an empty cache"""
        return {}

    def mock_json_load_newcache(self, file):
        """Mock an up to date cache"""
        new_time = datetime.datetime.now().timestamp()
        return {"timestamp": new_time, "bills": []}

    def mock_json_load_oldcache(self, file):
        """Mock an outdated cache"""
        old_time = datetime.datetime.now().timestamp() - (bills.CACHE_LIFE + 100)
        return {"timestamp": old_time}

    # pylint: disable=W0622
    # pylint: disable=R0913
    def mock_search_bills(
            self, state, updated_since, type, chamber, sort, search_window
    ):
        """Mock searching bills"""
        return [
            {
                "title": "BILL1",
                "updated_at": datetime.datetime.now(),
                "sponsors": [{"name": "JOE"}, {"name": "SAM"}],
                "actions": [{"action": "first"}, {"action": "second"}],
            },
            {
                "title": "BILL2",
                "updated_at": datetime.datetime.now(),
                "sponsors": [{"name": "KAT"}, {"name": "NICOLE"}],
                "actions": [{"action": "first"}, {"action": "second"}],
            },
        ]

    # pylint: disable=R0201
    # pylint: disable=R0916
    def test_get_cached_bills(self):
        """Make get_cached_bills test"""
        with mock.patch("json.load", self.mock_json_load_nocache):
            res = bills.get_cached_bills()
            self.assertIsNone(res)
        with mock.patch("json.load", self.mock_json_load_oldcache):
            res = bills.get_cached_bills()
            self.assertIsNone(res)
        with mock.patch("json.load", self.mock_json_load_newcache):
            res = bills.get_cached_bills()
            self.assertIsInstance(res, dict)

    def test_get_recent_bills_cached(self):
        """Make get_recent_bills test"""
        with mock.patch("json.load", self.mock_json_load_newcache):
            res = bills.get_recent_bills()
            self.assertIsInstance(res, dict)

    def test_get_recent_bills_new(self):
        """Make get_recent_bills test"""
        with mock.patch("json.load", self.mock_json_load_oldcache), mock.patch(
                "pyopenstates.search_bills", self.mock_search_bills
        ), mock.patch("builtins.open", mock.mock_open()):
            res = bills.get_recent_bills()
            self.assertIsInstance(res, dict)


if __name__ == "__main__":
    unittest.main()