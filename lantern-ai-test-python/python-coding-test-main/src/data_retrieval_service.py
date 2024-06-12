from typing import Dict, Callable, Union
import csv
import os

# Defines the type mapping for the existing data
CSV_FIELD_TYPES = {
    "Company Name": str,
    "Industry": str,
    "Market Capitalization": int,
    "Revenue (in millions)": int,
    "EBITDA (in millions)": int,
    "Net Income (in millions)": int,
    "Debt (in millions)": int,
    "Equity (in millions)": int,
    "Enterprise Value (in millions)": int,
    "P/E Ratio": float,
    "Revenue Growth Rate (%)": float,
    "EBITDA Margin (%)": float,
    "Net Income Margin (%)": float,
    "ROE (Return on Equity) (%)": float,
    "ROA (Return on Assets) (%)": float,
    "Current Ratio": float,
    "Debt to Equity Ratio": float,
    "Location": str,
}


class DataRetrievalService:
    def __init__(self):
        # Resolve the path to the database.csv file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = os.path.join(base_dir, "../data", "database.csv")

    def get_existing_data(self, company_name: str) -> Dict[str, Union[str, int, float]]:
        with open(self.database_path, mode="r") as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                if row["Company Name"] == company_name:
                    # Cast each field to its respective type
                    data = {
                        field: self._cast_value(value, CSV_FIELD_TYPES[field])
                        for field, value in row.items()
                    }
                    # Normalize location
                    if "Location" in data:
                        data["Location"] = self._normalize_location(data["Location"])
                    return data
        return None

    def _cast_value(self, value: str, cast_type: Callable) -> Union[str, int, float]:
        try:
            return cast_type(value)
        except ValueError:
            return value  # Return the original value if cast fails

    def _normalize_location(self, location: str) -> str:
        """Normalize the location data by removing minor differences."""
        return location.split(",")[0].strip()
