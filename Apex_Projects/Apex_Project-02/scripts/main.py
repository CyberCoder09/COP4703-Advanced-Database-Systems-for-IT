from scripts.database import get_db # Importing the get_db function from the database module, which is used to create a database session for interacting with the database
from scripts.models import User, Event, Ticket # Importing the User, Event, and Ticket models from the models module, which represent the database tables for users, events, and tickets
from sqlalchemy.orm import Session # Importing the Session class from SQLAlchemy, which is used to
from fastapi import FastAPI, Depends # Importing the FastAPI class and Depends function from the FastAPI framework, which are used to create the API application and manage dependencies

app = FastAPI(title="Apex Event Ticketing API") # Creating an instance of the FastAPI class, which will be used to define the API endpoints and run the application

@app.get("/") # Defining a GET endpoint at the root URL ("/") of the API
def root():
    return {"message": "Welcome to the Apex Event Ticketing API!"} # Returning a welcome message when the root endpoint is accessed\

@app.get("/health") # Defining a GET endpoint at the "/health" URL of the API
def health_check(db : Session = Depends(get_db)): # Defining a function to handle requests to the "/health" endpoint, which takes a database session as a dependency
    return {"status": "OK", "database": "connected"} # Returning a status message indicating that the API is healthy when the "/health" endpoint is accessed


@app.get("/users") # Defining a GET endpoint at the "/users" URL of the API
def get_users(db: Session = Depends(get_db)): # Defining a function to handle requests to the "/users" endpoint, which takes a database session as a dependency
    users = db.query(User).all() # Querying the database for all User records
    return users # Returning the list of users as the response to the API request

@app.get("/events") # Defining a GET endpoint at the "/events" URL of the API
def get_events(db: Session = Depends(get_db)): # Defining a function to handle requests to the "/events" endpoint, which takes a database session as a dependency
    events = db.query(Event).all() # Querying the database for all Event records
    return events # Returning the list of events as the response to the API request

@app.get("/tickets") # Defining a GET endpoint at the "/tickets" URL of the API
def get_tickets(db: Session = Depends(get_db)): # Defining a function to handle requests to the "/tickets" endpoint, which takes a database session as a dependency
    tickets = db.query(Ticket).all() # Querying the database for all Ticket records
    return tickets # Returning the list of tickets as the response to the API request
