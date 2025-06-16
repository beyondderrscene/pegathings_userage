import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestUserAPI(unittest.TestCase):

    def test_create_user_with_empty_name(self):
        """
        TC1: Should receive 500 error when the name is empty (IndexError).
        """
        response = client.post("/add/", params={"name": "", "age": 25})
        self.assertEqual(response.status_code, 422) # katanya 500 itu internal server error
        self.assertIn("detail", response.json())

    def test_create_user_with_age_999(self):
        """
        TC2: Should accept creation with age 999 (unless limited).
        """
        response = client.post("/add/", params={"name": "Bob", "age": 999})
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())

if __name__ == "__main__":
    unittest.main()
