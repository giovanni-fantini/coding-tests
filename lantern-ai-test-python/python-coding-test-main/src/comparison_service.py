from typing import Dict, Union


class ComparisonService:
    def __init__(self):
        pass

    def compare_data(
        self,
        extracted_data: Dict[str, Union[str, int, float]],
        existing_data: Dict[str, Union[str, int, float]],
    ) -> Dict:

        discrepancies = {}

        for field in extracted_data:
            extracted_value = extracted_data[field]
            existing_value = existing_data.get(field, None)

            # Normalize location data before comparing it
            if field == "Location":
                extracted_value = self._normalize_location(extracted_value)

            if extracted_value != existing_value:
                discrepancies[field] = {
                    "pdf_data": extracted_value,
                    "existing_data": existing_value,
                }

        return discrepancies

    def _normalize_location(self, location: str) -> str:
        """Normalize the location data by removing minor differences."""
        return location.split(",")[0].strip()
