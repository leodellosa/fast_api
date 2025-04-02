# Getting Started with FastAPI
Welcome to the FastAPI project! This README will guide you through the steps to get the project running locally on your machine.

## Prerequisites
Before you get started, ensure you have the following installed:
- Python 3.7+ (FastAPI requires Python 3.7 or later)
- pip (Python's package installer)
- FastAPI and Uvicorn for the ASGI server

To install FastAPI and Uvicorn, you can run:
- pip install fastapi uvicorn
or 
- pip install "fastapi[standard]"

### Running the Application
To run the FastAPI application, open a terminal and use the following command:
 - uvicorn main:app --reload
 or 
 - fastapi dev main.py

 This will start the development server with auto-reload enabled, so any changes you make will be automatically reflected without needing to restart the server.

**Note:** main refers to your Python file (e.g., main.py), and app refers to the FastAPI instance in your code.

### Access the Application
Once the server is running, open your browser and navigate to the following address:

Application Home: http://127.0.0.1:8000/

### Interactive API Docs
FastAPI automatically generates interactive API documentation using Swagger UI, which is a great way to test your API.
- Swagger UI (Interactive Docs): http://127.0.0.1:8000/docs

### Alternative API Docs
For a more traditional API documentation style, FastAPI also provides ReDoc, which is another option for viewing your API documentation.
- ReDoc Docs: http://127.0.0.1:8000/redoc

### OpenAPI Schema
FastAPI automatically generates an OpenAPI schema for your API. You can view this JSON file at the following URL:
- OpenAPI Schema: http://127.0.0.1:8000/openapi.json