## Solution Description

This FastAPI application provides an API endpoint for uploading PDF files, extracting relevant data from them, and comparing this data against existing data stored in a CSV file.

### Security
- **API Key Validation**: An API key is required and validated using FastAPI's `Depends` dependency injection.

### File Handling
- **PDF Upload Handling**: The `/upload` endpoint accepts a PDF file and a company name. It verifies the file format and safely writes the file to a predefined directory.
- **Path Resolution**: All file paths are resolved dynamically using absolute paths to ensure the application works correctly regardless of the current working directory.

### Data Extraction and Comparison
- **PDF Extraction**: Extracted data from the uploaded PDF is processed via a `PdfService`.
- **Existing Data Retrieval**: Existing company data is retrieved from a CSV file via a `DataRetrievalService`, with type casting and normalization.
- **Data Comparison**: The extracted and existing data are compared using a `ComparisonService`, identifying any discrepancies.

### Consistent Exception Handling
- **Error Responses**: The application handles various error scenarios with consistent HTTP exceptions and meaningful error messages, ensuring reliable client feedback.

### Documentation and Code Readability
- **OpenAPI docs**: The `/upload` endpoint includes includes detailed OpenAPI docs, facilitating easy understanding and usage for consumers.

### Key Endpoints
- **`GET /`**: A root endpoint that provides a simple status check for the API.
- **`POST /upload`**: The primary endpoint for uploading PDF files, extracting and comparing data against existing records, protected by API key authentication.

## Further Production Improvements and Notes
- **Base64-Encoded File Handling**: For a general-purpose API, we would enable receiving files as Base64-encoded strings within JSON payloads rather than using form-data, which assumes a web interface. This would necessitate providing clients with tooling for encoding their files appropriately. 
- **Leveraging Large Language Models (LLMs)**: In a production environment, LLMs could be employed to perform smarter and more flexible data discrepancy checks (e.g., ignoring minor spelling mistakes). The main focus for the service would be on effective prompt engineering to provide the LLM with the necessary information and requirements.
- **Authentication**: While authentication is present in a very simplistic way, in a real-world application, we would use an identity provider to validate API keys and ensure secure access.
- **Repository Structuring**: It is advisable to restructure the repository to leverage modules and packages, following established Python patterns. This will facilitate better file and dependency management.
- **Data Validation with Pydantic**: Integrating Pydantic data models to validate expected data fields and types will ensure that mandatory expected attributes match type specifications.
- **Containerization**: Containerizing the solution using tools like Docker will streamline deployment processes and ensure a standardized environment across different stages of development and production.
- **Parsing and Validation Enhancements**: Improvements could include more resilient handling of company names (considering case sensitivity) and adding support for new cases, such as PDFs that do not have existing data in the system.

## Example CURL command

curl -X POST "http://127.0.0.1:8000/upload" \
-H "Content-Type: multipart/form-data" \
-H "X-API-KEY: TEST_KEY" \
-F "file=@FILE_PATH" \
-F "company_name=COMPANY_NAME"

## Running tests
poetry run python src/tests.py