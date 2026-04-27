"""
Script para poblar la base de datos con datos de prueba.

Ejecutar una vez antes de probar la API.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.awesome_agent_api.infrastructure.db.database import SessionLocal, init_db
from src.awesome_agent_api.infrastructure.db.models import ProductModel
from datetime import datetime

def seed_products():
    """Inserta productos de prueba en la base de datos."""
    
    init_db()
    db = SessionLocal()
    
    # Verificar si ya hay datos
    existing = db.query(ProductModel).count()
    if existing > 0:
        print(f"Ya hay {existing} productos en la BD. Omitiendo seed.")
        db.close()
        return
    
    products = [
        ProductModel(
            name="Air Zoom Pegasus 40",
            brand="Nike",
            category="Running",
            size=42,
            color="Negro/Blanco",
            price=129.99,
            stock=15,
            description="Zapatilla de running con amortiguación responsive",
            created_at=datetime.now()
        ),
        ProductModel(
            name="Ultraboost 23",
            brand="Adidas",
            category="Running",
            size=41,
            color="Blanco",
            price=189.99,
            stock=8,
            description="Zapatilla premium con tecnología Boost",
            created_at=datetime.now()
        ),
        ProductModel(
            name="Chuck Taylor All Star",
            brand="Converse",
            category="Casual",
            size=43,
            color="Rojo",
            price=65.99,
            stock=20,
            description="Clásica zapatilla de lona para uso diario",
            created_at=datetime.now()
        ),
        ProductModel(
            name="Old Skool",
            brand="Vans",
            category="Skate",
            size=40,
            color="Negro/Blanco",
            price=75.99,
            stock=12,
            description="Zapatilla icónica con franja lateral",
            created_at=datetime.now()
        ),
        ProductModel(
            name="Suede Classic",
            brand="Puma",
            category="Casual",
            size=44,
            color="Azul Marino",
            price=89.99,
            stock=0,
            description="Clásica zapatilla de gamuza",
            created_at=datetime.now()
        ),
    ]
    
    db.add_all(products)
    db.commit()
    db.close()
    
    print(f"✅ {len(products)} productos insertados correctamente")

if __name__ == "__main__":
    seed_products()