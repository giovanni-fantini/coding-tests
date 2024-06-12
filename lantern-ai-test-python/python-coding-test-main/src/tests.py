import unittest
from fastapi.testclient import TestClient
import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import app

client = TestClient(app)
VALID_API_KEY = "TEST_KEY"
HEADERS = {"X-API-KEY": VALID_API_KEY}

# Resolve the assets directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "../assets")


class TestAPI(unittest.TestCase):

    def test_read_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    def test_upload_invalid_api_key(self):
        invalid_headers = {"X-API-KEY": "INVALID_KEY"}
        with open(os.path.join(ASSETS_DIR, "healthinc.pdf"), "rb") as file:
            response = client.post(
                "/upload",
                files={"file": file},
                data={"company_name": "HealthInc"},
                headers=invalid_headers,
            )
        self.assertEqual(response.status_code, 403)
        self.assertIn("Invalid API Key", response.json()["detail"])

    def test_upload_file_no_file(self):
        response = client.post(
            "/upload", data={"company_name": "HealthInc"}, headers=HEADERS
        )
        self.assertEqual(response.status_code, 422)

    def test_upload_invalid_file_format(self):
        invalid_file_path = os.path.join(ASSETS_DIR, "invalid_file.txt")
        with open(invalid_file_path, "wb") as f:
            f.write(b"Not a PDF content")
        with open(invalid_file_path, "rb") as file:
            response = client.post(
                "/upload",
                files={"file": file},
                data={"company_name": "HealthInc"},
                headers=HEADERS,
            )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid file format", response.json()["detail"])

    def test_upload_no_matching_company(self):
        with open(os.path.join(ASSETS_DIR, "healthinc.pdf"), "rb") as file:
            response = client.post(
                "/upload",
                files={"file": file},
                data={"company_name": "NonExistentCo"},
                headers=HEADERS,
            )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Company data not found", response.json()["detail"])

    def test_upload_successful_healthinc(self):
        with open(os.path.join(ASSETS_DIR, "healthinc.pdf"), "rb") as file:
            response = client.post(
                "/upload",
                files={"file": file},
                data={"company_name": "HealthInc"},
                headers=HEADERS,
            )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        expected_extracted_data = {
            "Company Name": "HealthInc",
            "Industry": "Healthcare",
            "Market Capitalization": 3000,
            "Revenue (in millions)": 1000,
            "EBITDA (in millions)": 250,
            "Net Income (in millions)": 80,
            "Debt (in millions)": 150,
            "Equity (in millions)": 666,
            "Enterprise Value (in millions)": 3150,
            "P/E Ratio": 15,
            "Revenue Growth Rate (%)": 12,
            "EBITDA Margin (%)": 40,
            "Net Income Margin (%)": 8,
            "ROE (Return on Equity) (%)": 13.33,
            "ROA (Return on Assets) (%)": 10,
            "Debt to Equity Ratio": 0.25,
            "Location": "New York, NY",
            "CEO": "Jane Smith",
            "Number of Employees": 3000,
        }

        expected_existing_data = {
            "Company Name": "HealthInc",
            "Industry": "Healthcare",
            "Market Capitalization": 3000,
            "Revenue (in millions)": 1000,
            "EBITDA (in millions)": 250,
            "Net Income (in millions)": 80,
            "Debt (in millions)": 150,
            "Equity (in millions)": 600,
            "Enterprise Value (in millions)": 3150,
            "P/E Ratio": 15.0,
            "Revenue Growth Rate (%)": 12.0,
            "EBITDA Margin (%)": 25.0,
            "Net Income Margin (%)": 8.0,
            "ROE (Return on Equity) (%)": 13.33,
            "ROA (Return on Assets) (%)": 10.0,
            "Current Ratio": 2.0,
            "Debt to Equity Ratio": 0.25,
            "Location": "New York",
        }

        expected_discrepancies = {
            "Equity (in millions)": {"pdf_data": 666, "existing_data": 600},
            "EBITDA Margin (%)": {"pdf_data": 40, "existing_data": 25.0},
            "CEO": {"pdf_data": "Jane Smith", "existing_data": None},
            "Number of Employees": {"pdf_data": 3000, "existing_data": None},
        }

        self.assertIn("extracted_data", response_json)
        self.assertIn("existing_data", response_json)
        self.assertIn("discrepancies", response_json)

        self.assertEqual(response_json["extracted_data"], expected_extracted_data)
        self.assertEqual(response_json["existing_data"], expected_existing_data)
        self.assertEqual(response_json["discrepancies"], expected_discrepancies)


if __name__ == "__main__":
    unittest.main()
