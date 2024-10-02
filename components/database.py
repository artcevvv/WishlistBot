from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, URL, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()   

POSTGRES_SQL_PASS = os.getenv("POSTGRES_SQL_PASS")

POSTGRES_SQL_URL = URL.create(
    "postgresql",
    username="postgres",
    password=POSTGRES_SQL_PASS,
    host="localhost",
    port=5432,
    database="wishyourpartner",
)

engine = create_engine(POSTGRES_SQL_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(BigInteger, unique=True, index=True)
    telegram_user_name = Column(String, unique=True, index=True)
    partner_user_name = Column(String, nullable=True, index=True)  # Partner's Telegram username
    created_at = Column(DateTime, default=datetime.now())
    
    # One-to-many relationship with wishes
    wishes = relationship("Wishes", back_populates="owner", cascade="all, delete-orphan")

class Wishes(Base):
    __tablename__ = "wishes"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String, nullable=True)  # Image URL (optional)
    text = Column(String, nullable=False)  # Wish text
    link = Column(String, nullable=True)   # Link (optional)
    description = Column(String, nullable=True)  # Description (optional)
    created_at = Column(DateTime, default=datetime.now())
    
    # Foreign key to reference the owner (user)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ForeignKey added here
    owner = relationship("User", back_populates="wishes")

# Create all tables
Base.metadata.create_all(bind=engine)
    