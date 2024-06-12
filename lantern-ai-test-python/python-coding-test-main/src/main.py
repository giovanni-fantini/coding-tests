import os
from fastapi import FastAPI, UploadFile, Form, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from src.pdf_service import PdfService
from src.comparison_service import ComparisonService
from src.data_retrieval_service import DataRetrievalService

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "../assets")
VALID_API_KEY = os.getenv("VALID_API_KEY", "TEST_KEY") 

# Initialize services
pdf_service = PdfService(VALID_API_KEY)
data_retrieval_service = DataRetrievalService()
comparison_service = ComparisonService()

app = FastAPI()

# Security
api_key_header = APIKeyHeader(name="X-API-KEY")

def get_api_key(api_key: str = Depends(api_key_header)) -> str:
    """Validate the provided API key."""
    if api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key"
        )
    return api_key

@app.post(
    "/upload",
    summary="Upload a PDF for data extraction and comparison",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "extracted_data": {
                            "Company_Name": "FinanceLLC",
                            "Industry": "Financial Services",
                            "Market_Capitalization": 4500,
                            "Revenue_in_millions": 1200,
                            "Enterprise Value (in millions)": 4400,
                            "ROA_Return_on_Assets": 12.0,
                            "Current_Ratio": 3.0,
                            "Location": "Boston, MA",
                            "CEO": "Alice Brown",
                            "Number_of_Employees": 1500,
                        },
                        "existing_data": {
                            "Company_Name": "FinanceLLC",
                            "Industry": "Financial Services",
                            "Market_Capitalization": 4000,
                            "Revenue_in_millions": 1200,
                            "Enterprise Value (in millions)": 4300,
                            "ROA_Return_on_Assets": 12,
                            "Current_Ratio": 3,
                            "Location": "Boston",
                        },
                        "discrepancies": {
                            "Market_Capitalization": {
                                "pdf_data": 4500,
                                "existing_data": 4000,
                            },
                            "Enterprise Value (in millions)": {
                                "pdf_data": 4400,
                                "existing_data": 4300,
                            },
                            "CEO": {"pdf_data": "Alice Brown", "existing_data": None},
                            "Number_of_Employees": {
                                "pdf_data": 1500,
                                "existing_data": None,
                            },
                        },
                    }
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid file format. Only PDF files are allowed."
                    }
                }
            },
        },
        403: {
            "description": "Forbidden",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        },
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {"example": {"detail": "Company data not found"}}
            },
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Request parameters are missing or invalid"}
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to save the uploaded file."}
                }
            },
        },
    },
    dependencies=[Depends(get_api_key)],
)
async def upload_file(file: UploadFile, company_name: str = Form(...)):
    """
    Upload a PDF file containing company data.

    The file will be processed to extract data via a third-party PDF extraction service,
    and the extracted data will be compared against existing data stored in the CSV file.

    - **file**: The PDF file containing the company data.
    - **company_name**: The name of the company to retrieve existing data for comparison.
    """

    if not (file.filename.endswith(".pdf") and file.content_type == "application/pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF files are allowed.",
        )

    file_location = os.path.join(ASSETS_DIR, file.filename)

    try:
        with open(file_location, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save the uploaded file.",
        ) from e

    try:
        extracted_data = pdf_service.extract(f"assets/{file.filename}")
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDF extraction failed. Invalid file provided.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="PDF extraction service failed.",
        ) from e

    try:
        existing_data = data_retrieval_service.get_existing_data(company_name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve existing data.",
        ) from e

    if existing_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company data not found"
        )

    discrepancies = comparison_service.compare_data(extracted_data, existing_data)

    return JSONResponse(
        content={
            "extracted_data": extracted_data,
            "existing_data": existing_data,
            "discrepancies": discrepancies,
        },
        status_code=status.HTTP_200_OK,
    )


@app.get("/", summary="Root endpoint", response_description="Check the API status")
def read_root():
    """
    Root endpoint to check the status of the API.
    """
    return {"Hello": "World"}
