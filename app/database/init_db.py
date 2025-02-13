from app.database.db import engine, Base
from app.models.user import User
from app.models.order import Order

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
