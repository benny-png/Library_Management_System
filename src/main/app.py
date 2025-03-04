from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from src.main.routes import users, books
from src.database.models import create_tables

# Create the tables
create_tables()

# Load env here if needed using config if defined
app = FastAPI(
    title="Library Management System",
    description="A simple library management system API",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(users.users_router)
app.include_router(books.books_router, tags=["books"])


# General middleware for the application