from sqlalchemy.orm import Session
from scripts.models import User, Event, Ticket


class UserRepository:
    def __init__(self, session: Session):
        self.session = session  # Store the session so methods can use it

    def get_all(self):
        return self.session.query(User).all()  # The query that USED to live in main.py

    def get_by_id(self, user_id: int):
        return (
            self.session.query(User).filter(User.id == user_id).first()
        )  # Query to get a user by ID

    def get_by_email(self, email: str):
        return (
            self.session.query(User).filter(User.email == email).first()
        )  # Query to get a user by email

    def add(self, user: User):
        self.session.add(user)  # Add a new user to the session

    def delete(self, user: User):
        self.session.delete(user)  # Delete a user from the session


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Event).all()

    def get_by_id(self, event_id: int):
        return self.session.query(Event).filter(Event.id == event_id).first()

    def add(self, event: Event):
        self.session.add(event)

    def delete(self, event: Event):
        self.session.delete(event)


class TicketRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Ticket).all()

    def get_by_id(self, ticket_id: int):
        return self.session.query(Ticket).filter(Ticket.id == ticket_id).first()

    def get_by_event_id(self, event_id: int):
        return self.session.query(Ticket).filter(Ticket.event_id == event_id).all()

    def get_by_user_id(self, user_id: int):
        return self.session.query(Ticket).filter(Ticket.user_id == user_id).all()

    def get_by_event_and_user(self, event_id: int, user_id: int):
        return (
            self.session.query(Ticket)
            .filter(Ticket.event_id == event_id, Ticket.user_id == user_id)
            .first()
        )

    def add(self, ticket: Ticket):
        self.session.add(ticket)

    def delete(self, ticket: Ticket):
        self.session.delete(ticket)
