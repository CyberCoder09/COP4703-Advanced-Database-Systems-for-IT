from scripts.database import SessionLocal
from scripts.repositories import UserRepository, EventRepository, TicketRepository


class UnitOfWork:
    def __enter__(self):
        self.session = SessionLocal()  # Open a session when entering the `with` block

        self.users = UserRepository(self.session)  # Hand the session to each repo
        self.events = EventRepository(self.session)
        self.tickets = TicketRepository(self.session)
        return self  # Return self so routes can do `uow.users.get_all()`

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:  # If something went wrong inside the `with` block...
            self.session.rollback()  # ...undo any changes
        self.session.close()  # Always close the session when done

    def commit(self):
        self.session.commit()  # Commit changes to the database

    def rollback(self):
        self.session.rollback()  # Rollback changes in case of an error
