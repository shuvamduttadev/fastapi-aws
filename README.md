
# FastAPI Project

This is a FastAPI project showcasing a structured approach to building RESTful APIs.

## Setup

1.  Clone the repository.
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the virtual environment: `source venv/Scripts/activate` (Windows: `venv\Scripts\activate`)
4.  Install dependencies: `pip install -r requirements.txt`
5.  Copy `.env.example` to `.env` and fill in your environment variables.
6.  Run database migrations:
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
    ```
7.  Run the application: `uvicorn app.main:app --reload`

## Docker

To run the application using Docker:

1.  Build the Docker image: `docker-compose build`
2.  Start the services: `docker-compose up`
