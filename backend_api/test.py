from main import app
import unittest

# create your unit tests here.

class TestRoutes(unittest.TestCase):
    # check for 200 & json response
    def test_ifsc_query(self):
        client = app.test_client(self)
        response = client.get('/ifsc-search?ifsc_code=ABHY0065005')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    # check for 200 & json response
    def test_bank_leaderboard_query(self):
        client = app.test_client(self)
        response = client.get('/leaderboard?sortorder=ASC&fetchcount=3')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    # check for 200 & json response
    def test_statistics_query(self):
        client = app.test_client(self)
        response = client.get('/statistics?sortorder=DESC&fetchcount=7')
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(response.content_type, "application/json")


if __name__ == "__main__":
    unittest.main()