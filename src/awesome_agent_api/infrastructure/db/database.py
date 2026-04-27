"""
Configuración de la base de datos SQLite.

Maneja la conexión y sesiones de SQLAlchemy.
"""

import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

# Base para modelos ORM
Base = declarative_base()


def get_database_url() -> str:
    """
    Obtiene la URL de la base de datos.
    
    Returns:
        URL de conexión a SQLite
    """
    db_path = os.getenv("DATABASE_URL", "sqlite:///./data/products.db")
    return db_path


def create_db_engine():
    """
    Crea el engine de SQLAlchemy.
    
    Returns:
        Engine configurado
    """
    url = get_database_url()
    
    # Configuración para SQLite con soporte a foreign keys
    engine = create_engine(
        url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False
    )
    
    # Habilitar foreign keys en SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
    return engine


# Crear engine y session factory
engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Generador de sesiones para inyección de dependencias.
    
    Yields:
        Sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas.
    
    Debe llamarse una vez al inicio de la aplicación.
    """
    Base.metadata.create_all(bind=engine)