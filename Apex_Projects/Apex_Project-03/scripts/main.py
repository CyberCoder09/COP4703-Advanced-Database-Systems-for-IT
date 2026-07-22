from scripts.models import (
    User,
    Event,
    Ticket,
)  # Importing the User, Event, and Ticket models from the models module, which represent the database tables for users, events, and tickets
from scripts.unit_of_work import (
    UnitOfWork,
)  # Importing the UnitOfWork class from the unit_of_work module, which is used to manage database transactions and ensure that changes are committed or rolled back as a single unit of work
from fastapi import (
    FastAPI,
    HTTPException,
)  # Importing the FastAPI class & Depends function from the FastAPI framework, which are used to create the API application and manage dependencies
from datetime import (
    datetime,
)  # Importing the datetime class from the datetime module, which is used to work with date and time values
from decimal import (
    Decimal,
)  # Importing the Decimal class from the decimal module, which is used to work with decimal numbers for precise financial calculations
from pydantic import (
    BaseModel,
)  # Importing the BaseModel class from Pydantic, which is used to define data models for request validation and response serialization

# Creating an instance of the FastAPI class, which will be used to define the API endpoints and run the application
app = FastAPI(title="Apex Event Ticketing API")


class UserCreate(
    BaseModel
):  # Defining a Pydantic model for creating a new user, which will be used to validate the request body for the create_user endpoint
    name: str  # The name of the user, which is a required string field
    email: str  # The email of the user, which is a required string field
    phone_number: str  # The phone number of the user, which is a required string field


class EventCreate(
    BaseModel
):  # Defining a Pydantic model for creating a new event, which will be used to validate the request body for the create_event endpoint
    name: str  # The name of the event, which is a required string field
    date: datetime  # The date of the event, which is a required datetime field
    location: str  # The location of the event, which is a required string field


class TicketCreate(
    BaseModel
):  # Defining a Pydantic model for creating a new ticket, which will be used to validate the request body for the create_ticket endpoint
    event_id: int  # The ID of the event for which the ticket is being created, which is a required integer field
    user_id: int  # The ID of the user who is purchasing the ticket, which is a required integer field
    price: Decimal  # The price of the ticket, which is a required decimal field
    ticket_type: str  # The type of the ticket (e.g., VIP, General Admission), which is a required string field
    status: str = (
        "active"  # The status of the ticket (e.g., available, sold), which is a required string field
    )


@app.get(
    "/"
)  # Defining a GET endpoint at the root URL ("/") of the API, which will return a welcome message when accessed
def root():  # Defining the function that will be executed when the root endpoint is accessed
    return {
        "message": "Welcome to the Apex Event Ticketing API!"
    }  # Returning a JSON response with a welcome message


@app.get(
    "/health"
)  # Defining a GET endpoint at the "/health" URL of the API, which will return a health check message when accessed
def health_check():  # Defining the function that will be executed when the health check endpoint is accessed
    return {
        "status": "healthy",
        "database": "connected",
        "message": "API is running smoothly.",
    }  # Returning a JSON response indicating that the API is healthy


@app.get(
    "/users"
)  # Defining a GET endpoint at the "/users" URL of the API, which will return a list of all users when accessed
def get_users():  # Defining the function that will be executed when the get_users endpoint is accessed
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        users = (
            uow.users.get_all()
        )  # Using the UserRepository to retrieve all users from the database
        return users  # Returning the list of users as a JSON response


@app.get(
    "/users/{user_id}"
)  # Defining a GET endpoint at the "/users" URL of the API, which will return a list of all users when accessed
def get_users_by_id(
    user_id: int,
):  # Defining the function that will be executed when the get_users endpoint is accessed
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        user = uow.users.get_by_id(
            user_id
        )  # Using the UserRepository to retrieve a user by their ID from the database
        if not user:
            raise HTTPException(
                status_code=404, detail="User not found"
            )  # Raising an HTTP 404 error if the user is not found
        return user  # Returning the user as a JSON response


@app.post(
    "/users"
)  # Defining a POST endpoint at the "/users" URL of the API, which will create a new user when accessed
def create_user(
    user_data: UserCreate,
):  # Defining the function that will be executed when the create_user endpoint is accessed, with the request body validated against the UserCreate model
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        existing_user = uow.users.get_by_email(
            user_data.email
        )  # Checking if a user with the same email already exists in the database
        if existing_user:  # If an existing user is found...
            raise HTTPException(
                status_code=400, detail="Email already registered"
            )  # ...raise an HTTP 400 error indicating that the email is already registered

        user = User(
            name=user_data.name,
            email=user_data.email,
            phone_number=user_data.phone_number,
        )  # Creating a new User instance with the provided data
        uow.users.add(user)  # Adding the new user to the database session
        uow.commit()  # Committing the transaction to save the new user to the database
        uow.session.refresh(user)
        return user


@app.get(
    "/events"
)  # Defining a GET endpoint at the "/events" URL of the API, which will return a list of all events when accessed
def get_events():  # Defining the function that will be executed when the get_events endpoint is accessed
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        events = (
            uow.events.get_all()
        )  # Using the EventRepository to retrieve all events from the database
        return events  # Returning the list of events as a JSON response


@app.get(
    "/events/{event_id}"
)  # Defining a GET endpoint at the "/events" URL of the API, which will return a specific event when accessed
def get_events_by_id(
    event_id: int,
):  # Defining the function that will be executed when the get_events_by_id endpoint is accessed
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        event = uow.events.get_by_id(
            event_id
        )  # Using the EventRepository to retrieve an event by its ID from the database
        if not event:
            raise HTTPException(
                status_code=404, detail="Event not found"
            )  # Raising an HTTP 404 error if the event is not found
        return event  # Returning the event                                           as a JSON response


@app.post(
    "/events"
)  # Defining a POST endpoint at the "/events" URL of the API, which will create a new event when accessed
def create_event(
    event_data: EventCreate,
):  # Defining the function that will be executed when the create_event endpoint is accessed, with the request body validated against the EventCreate model
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        event = Event(
            name=event_data.name, date=event_data.date, location=event_data.location
        )  # Creating a new Event instance with the provided data
        uow.events.add(event)  # Adding the new event to the database session
        uow.commit()  # Committing the transaction to save the new event to the database
        uow.session.refresh(event)
        return event  # Returning the newly created event as a JSON response


@app.get(
    "/tickets"
)  # Defining a GET endpoint at the "/tickets" URL of the API, which will return a list of all tickets when accessed
def get_tickets():  # Defining the function that will be executed when the get_tickets endpoint is accessed
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        tickets = (
            uow.tickets.get_all()
        )  # Using the TicketRepository to retrieve all tickets from the database
        return tickets  # Returning the list of tickets as a JSON response


@app.get(
    "/tickets/{ticket_id}"
)  # Defining a GET endpoint at the "/tickets/{ticket_id}" URL of the API, which will return a specific ticket when accessed
def get_tickets_by_id(
    ticket_id: int,
):  # Defining the function that will be executed when the get_tickets_by_id endpoint is accessed
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        ticket = uow.tickets.get_by_id(
            ticket_id
        )  # Using the TicketRepository to retrieve a ticket by its ID from the database
        if not ticket:
            raise HTTPException(
                status_code=404, detail="Ticket not found"
            )  # Raising an HTTP 404 error if the ticket is not found
        return ticket  # Returning the ticket as a JSON response


@app.post(
    "/tickets"
)  # Defining a POST endpoint at the "/tickets" URL of the API, which will create a new ticket when accessed
def create_ticket(
    ticket_data: TicketCreate,
):  # Defining the function that will be executed when the create_ticket endpoint is accessed, with the request body validated against the TicketCreate model
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        user = uow.users.get_by_id(
            ticket_data.user_id
        )  # Retrieving the user associated with the ticket from the database
        if not user:  # If the user does not exist...
            raise HTTPException(
                status_code=404, detail="User not found"
            )  # ...raise an HTTP 404 error indicating that the user was not found
        event = uow.events.get_by_id(
            ticket_data.event_id
        )  # Retrieving the event associated with the ticket from the database
        if not event:  # If the event does not exist...
            raise HTTPException(
                status_code=404, detail="Event not found"
            )  # ...raise an HTTP 404 error indicating that the event was not found
        existing_ticket = uow.tickets.get_by_event_and_user(
            ticket_data.event_id, ticket_data.user_id
        )  # Checking if a ticket for the same event and user already exists in the database
        if existing_ticket:  # If an existing ticket is found...
            raise HTTPException(
                status_code=400, detail="Ticket already exists for this user and event"
            )  # ...raise an HTTP 400 error indicating that the ticket already exists
        ticket = Ticket(
            event_id=ticket_data.event_id,
            user_id=ticket_data.user_id,
            price=ticket_data.price,
            ticket_type=ticket_data.ticket_type,
            status=ticket_data.status,
        )  # Creating a new Ticket instance with the provided data
        uow.tickets.add(ticket)  # Adding the new ticket to the database session
        uow.commit()  # Committing the transaction to save the changes to the database
        uow.session.refresh(
            ticket
        )  # Refreshing the ticket instance with the latest data from the database
        return ticket  # Returning the created ticket as a JSON response


@app.delete(
    "/users/{user_id}"
)  # Defining a DELETE endpoint at the "/users/{user_id}" URL of the API, which will delete a specific user when accessed
def delete_user(
    user_id: int,
):  # Defining the function that will be executed when the delete_user endpoint is accessed
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        user = uow.users.get_by_id(
            user_id
        )  # Using the UserRepository to retrieve a user by their ID from the database
        if not user:  # If the user does not exist...
            raise HTTPException(
                status_code=404, detail="User not found"
            )  # ...raise an HTTP 404 error indicating that the user was not found
        uow.users.delete(user)  # Deleting the user from the database session
        uow.commit()  # Committing the transaction to save the changes to the database
        return {
            "message": "User deleted successfully"
        }  # Returning a success message as a JSON response


@app.delete(
    "/events/{event_id}"
)  # Defining a DELETE endpoint at the "/events/{event_id}" URL of the API, which will delete a specific event when accessed
def delete_event(
    event_id: int,
):  # Defining the function that will be executed when the delete_event endpoint is accessed
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        event = uow.events.get_by_id(
            event_id
        )  # Using the EventRepository to retrieve an event by its ID from the database
        if not event:  # If the event does not exist...
            raise HTTPException(
                status_code=404, detail="Event not found"
            )  # ...raise an HTTP 404 error indicating that the event was not found
        uow.events.delete(event)  # Deleting the event from the database session
        uow.commit()  # Committing the transaction to save the changes to the database
        return {
            "message": "Event deleted successfully"
        }  # Returning a success message as a JSON response


@app.delete(
    "/tickets/{ticket_id}"
)  # Defining a DELETE endpoint at the "/tickets/{ticket_id}" URL of the API, which will delete a specific ticket when accessed
def delete_ticket(
    ticket_id: int,
):  # Defining the function that will be executed when the delete_ticket endpoint is accessed
    with UnitOfWork() as uow:  # Creating a new UnitOfWork instance to manage the database session and transactions
        ticket = uow.tickets.get_by_id(
            ticket_id
        )  # Using the TicketRepository to retrieve a ticket by its ID from the database
        if not ticket:  # If the ticket does not exist...
            raise HTTPException(
                status_code=404, detail="Ticket not found"
            )  # ...raise an HTTP 404 error indicating that the ticket was not found
        uow.tickets.delete(ticket)  # Deleting the ticket from the database session
        uow.commit()  # Committing the transaction to save the changes to the database
        return {
            "message": "Ticket deleted successfully"
        }  # Returning a success message as a JSON response
