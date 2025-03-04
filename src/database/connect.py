"""
Database connection logic goes here

- Connect to the database

Keep the database URL in the .env file

"""

import os

from sqlmodel import create_engine
from sqlalchemy.engine import Engine


class Connect:
    """
    This handles the connection to the database
    """

    @staticmethod
    def get_database_url() -> str:
        """
        Get database url depending on environment set up:

        Make sure you have set up your variables in .env

        This assumes you have set up your database URL in the .env file
        """

        if os.getenv("DEVELOPMENT_MODE", "false").lower() == "true":
            if url := os.getenv("DEV_DATABASE_URL"):
                database_url = url
            else:
                # Use the /app/data directory for SQLite database
                sqlite_file_name = "/app/data/database.db"
                database_url = f"sqlite:///{sqlite_file_name}"
        else:
            database_url = os.getenv("PROD_DATABASE_URL", "")
            if not database_url:
                # Use the /app/data directory for SQLite database in production
                sqlite_file_name = "/app/data/database.db"
                database_url = f"sqlite:///{sqlite_file_name}"

        return database_url

    @staticmethod
    def connect() -> Engine:
        """
        Connect to the database.

        This is the main function that should be called to connect to the database
        """
        database_url = Connect.get_database_url()
        # Engine accepts more parameters like pool_size, max_overflow, pool_recycle, etc.
        engine = create_engine(database_url, echo=True)
        return engine
