from fastapi import FastAPI
from app.db.database import init_database, close_database


def startup_event():
    # Initialize the database connection
    init_database()


def shutdown_event():
    # Close the database connection
    close_database()


def register_events(app: FastAPI):
    app.add_event_handler("startup", startup_event)
    app.add_event_handler("shutdown", shutdown_event)
