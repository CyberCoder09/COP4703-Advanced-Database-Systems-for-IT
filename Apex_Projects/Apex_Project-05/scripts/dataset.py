import random
from decimal import Decimal

# This script populates the database with sample data for Users, Events, and Tickets.
from datetime import datetime, timedelta 
from faker import Faker # Import the Faker library to generate fake data for testing purposes
from scripts.database import SessionLocal      # Import the SessionLocal class from the database module to create a database session
from scripts.models import User, Event, Ticket # Import the User, Event, & Ticket models from the models module to create instances of these models


fake = Faker() # Create an instance of the Faker class to generate fake data

Faker.seed(42) # Seed the Faker library to ensure that the generated fake data is consistent across runs
random.seed(42) # Seed the random module to ensure that the generated random data is consistent across runs 

NUM_USERS = 10000 # Define the number of users and events to be created in the database
NUM_EVENTS = 100  # Define the number of users and events to be created in the database
BATCH_SIZE = 5000 # Define the number of records to be inserted in each batch when populating the database

db = SessionLocal() # Create a new database session using the SessionLocal class

# Define a function to create users in the database
def create_users():
    # Check if the number of users in the database is greater than or equal to NUM_USERS. 
    # If so, print a message & return.
    if db.query(User).count() >= NUM_USERS:
        print("Users already exist.") # 
        return

    print("Creating Users...")

    users = []

    for i in range(NUM_USERS):

        users.append(
            User(
                name=fake.name(),
                email=fake.unique.email(),
                phone_number=fake.phone_number()[:20],
            )
        )

        if len(users) == BATCH_SIZE:
            db.bulk_save_objects(users)
            db.commit()
            print(f"Inserted {i + 1} users")
            users = []

    if users:
        db.bulk_save_objects(users)
        db.commit()

    print("Users Completed.\n")


def create_events():

    if db.query(Event).count() >= NUM_EVENTS:
        print("Events already exist.")
        return

    print("Creating Events...")

    events = []

    event_names = [
        "AI Conference",
        "Music Festival",
        "Tech Expo",
        "Startup Summit",
        "Cricket Finals",
        "Football Championship",
        "Food Carnival",
        "Art Exhibition",
        "Gaming Tournament",
        "Movie Premiere",
    ]

    for i in range(NUM_EVENTS):

        events.append(
            Event(
                name=random.choice(event_names) + f" {i+1}",
                date=fake.date_time_between(
                    start_date="+1d",
                    end_date="+365d",
                ),
                location=f"{fake.city()}, {fake.country()}",
                price=Decimal(str(random.randint(20, 300))),
                total_capacity=10000,
                seats_available=10000,
            )
        )

        if len(events) == BATCH_SIZE:
            db.bulk_save_objects(events)
            db.commit()
            print(f"Inserted {i + 1} events")
            events = []

    if events:
        db.bulk_save_objects(events)
        db.commit()

    print("Events Completed.\n")

def create_tickets():

    total_tickets = db.query(Ticket).count()

    if total_tickets >= NUM_USERS * NUM_EVENTS:
        print("Tickets already exist.")
        return

    print("Creating Tickets...")

    tickets = []
    count = 0

    ticket_types = [
        "Regular",
        "VIP",
        "Student",
    ]

    ticket_status = [
        "active",
        "used",
    ]

    for user_id in range(1, NUM_USERS + 1):

        for event_id in range(1, NUM_EVENTS + 1):

            tickets.append(
                Ticket(
                    user_id=user_id,
                    event_id=event_id,
                    ticket_type=random.choice(ticket_types),
                    status=random.choice(ticket_status),
                )
            )

            count += 1

            if len(tickets) >= BATCH_SIZE:

                db.bulk_save_objects(tickets)
                db.commit()

                print(f"Inserted {count:,} tickets")

                tickets = []

    if tickets:

        db.bulk_save_objects(tickets)
        db.commit()

    print(f"\nFinished creating {count:,} tickets.\n") # Print the total number of tickets created

#
def main():
    create_users()   # Call the create_users function to populate the database with users
    create_events()  # Call the create_events function to populate the database with events
    create_tickets() # Call the create_tickets function to populate the database with tickets after users and events have been created
    db.close()       # Close the database session after all operations are completed to free up resources
    print("Dataset creation completed successfully.") # Print a success message

# 
if __name__ == "__main__":
    main() # Call the main function to start the dataset creation process
