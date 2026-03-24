from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

import streamlit as st

from config import Config

def get_engine():
    # Ensure data directory exists (only for SQLite)
    if Config.is_sqlite():
        # logic to make dir
        db_path = Config.DATABASE_URL.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        return create_engine(
            Config.DATABASE_URL, 
            connect_args={"check_same_thread": False},
            echo=Config.DB_ECHO
        )
    else:
        # Postgres
        return create_engine(
            Config.DATABASE_URL,
            pool_pre_ping=True,
            pool_size=Config.DB_POOL_SIZE,
            max_overflow=Config.DB_MAX_OVERFLOW,
            echo=Config.DB_ECHO
        )

engine = get_engine()

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency for getting DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
