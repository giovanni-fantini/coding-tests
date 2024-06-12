# Use this dummy service to extract data from PDF's

# DO NOT EDIT THIS FILE


class PdfService:

    def __init__(self, key: str):
        assert key == "TEST_KEY"
        self.key = key

    def extract(self, file_path: str):

        if file_path == "assets/healthinc.pdf":
            return {
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

        if file_path == "assets/retailco.pdf":
            return {
                "Company Name": "RetailCo",
                "Industry": "Retail",
                "Market Capitalization": 2000,
                "Revenue (in millions)": 800,
                "EBITDA (in millions)": 150,
                "Net Income (in millions)": 40,
                "Debt (in millions)": 110,
                "Equity (in millions)": 400,
                "Enterprise Value (in millions)": 2100,
                "P/E Ratio": 20,
                "Revenue Growth Rate (%)": 8,
                "EBITDA Margin (%)": 18.75,
                "ROE (Return on Equity) (%)": 10,
                "ROA (Return on Assets) (%)": 6.5,
                "Current Ratio": 1.8,
                "Debt to Equity Ratio": 0.25,
                "Location": "Chicago, IL",
                "CEO": "Bob Johnson",
                "Number of Employees": 2000,
            }

        if file_path == "assets/financellc.pdf":
            return {
                "Company Name": "FinanceLLC",
                "Industry": "Financial Services",
                "Market Capitalization": 4500,
                "Revenue (in millions)": 1200,
                "EBITDA (in millions)": 400,
                "Net Income (in millions)": 150,
                "Debt (in millions)": 300,
                "Equity (in millions)": 1000,
                "Enterprise Value (in millions)": 4400,
                "P/E Ratio": 18,
                "Revenue Growth Rate (%)": 15,
                "EBITDA Margin (%)": 33.33,
                "ROE (Return on Equity) (%)": 20,
                "ROA (Return on Assets) (%)": 12,
                "Current Ratio": 3,
                "Debt to Equity Ratio": 0.3,
                "Location": "Boston, MA",
                "CEO": "Alice Brown",
                "Number of Employees": 1500,
            }

        raise FileNotFoundError("Cannot extract data. Invalid file provided.")
