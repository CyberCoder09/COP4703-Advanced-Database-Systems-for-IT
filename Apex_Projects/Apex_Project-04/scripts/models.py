from sqlalchemy.orm import (
    relationship,
)  # Importing necessary components from SQLAlchemy for defining database models
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    func,
)

# Importing specific data types for defining columns in the database models
from scripts.database import Base  # Importing the Base class from the database module


# Defining the User model, which represents a user in the database
class User(Base):
    __tablename__ = (
        "users"  # Name of the table in the database that this model represents
    )

    id = Column(
        Integer, primary_key=True, index=True
    )  # Primary key column for the User model, automatically incrementing integer
    name = Column(String, nullable=False)  # Name cannot be null
    email = Column(
        String, nullable=False, unique=True
    )  # Email must be unique and cannot be null
    phone_number = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )  # Timestamp for when the user was created, cannot be null
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )  # Timestamp for when the user was
    tickets = relationship(
        "Ticket", back_populates="user"
    )  # Establishing a relationship between the User and Ticket models, allowing for easy access to a user's tickets


# Defining the Event model, which represents an event in the database
class Event(Base):
    __tablename__ = (
        "events"  # Name of the table in the database that this model represents
    )
    id = Column(Integer, primary_key=True)     # Primary key column for the Event model, automatically incrementing integer
    name = Column(String, nullable=False)      # Name of the event, cannot be null
    date = Column(DateTime, nullable=False)    # Date & time of the event, cannot be null
    location = Column(String, nullable=False)  # Location of the event, cannot be null
    price = Column(Numeric(10, 2), nullable=False, default=0.00) # Price of the event, cannot be null, defaulting to 0.00 if not specified

    # Capacity handling to prevent double booking/overbooking
    total_capacity = Column(Integer, nullable=False, default=100) # This column defines the total capacity of the event, ensuring that ticket sales do not exceed this limit.
    seats_available = Column(Integer, nullable=False, default=100) # This column tracks the number of seats available for the event, ensuring that ticket sales do not exceed the total capacity.

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) # Timestamp for when the event was created, cannot be null
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False) # Timestamp for when the event was last updated, cannot be null

    tickets = relationship("Ticket", back_populates="event") # Establishing a relationship between the Event and Ticket models, allowing for easy access to an event's tickets


class Ticket(Base):
    __tablename__ = (
        "tickets"  # Name of the table in the database that this model represents
    )
    id = Column(
        Integer, primary_key=True
    )  # Primary key column for the Ticket model, automatically incrementing integer
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Foreign key column referencing the User model, cannot be null
    event_id = Column(
        Integer, ForeignKey("events.id"), nullable=False
    )  # Foreign key column referencing the Event model, cannot be null
    ticket_type = Column(String, nullable=False)  # Type of the ticket, cannot be null
    status = Column(
        String, nullable=False, default="active"
    )  # Status of the ticket (e.g., "active", "sold"), cannot be null

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )  # Timestamp for when the ticket was created, cannot be null
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )  # Timestamp for when the ticket was last updated, cannot be null

    user = relationship(
        "User", back_populates="tickets"
    )  # Establishing a relationship between the Ticket & User models, allowing for easy access to the user associated with a ticket
    event = relationship(
        "Event", back_populates="tickets"
    )  # Establishing a relationship between the Ticket and Event models, allowing for easy access to the event associated with a ticket

    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="unique_user_event"),
    )  # Adding a unique constraint to ensure that a user can only have one ticket for a specific event, preventing duplicate entries in the tickets table for the same user & event combination
