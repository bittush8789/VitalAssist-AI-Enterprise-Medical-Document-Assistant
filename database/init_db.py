from database.db import engine, Base
from database.models import User, Patient, Report, AuditLog

def init_db():
    print("Initializing Database...")
    Base.metadata.create_all(bind=engine)
    print("Database Initialized!")

if __name__ == "__main__":
    init_db()
