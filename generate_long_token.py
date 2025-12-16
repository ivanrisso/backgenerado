
import asyncio
from datetime import timedelta
from app.infrastructure.security.jwt_handler import create_access_token

async def generate_token():
    # Email for admin user
    email = "admin@facturacion.com"
    data = {"sub": email, "type": "access"}
    
    # 365 days expiration
    expires = timedelta(days=365)
    token = create_access_token(data, expires_delta=expires)
    
    print("\n========================================================")
    print("TOKEN DE LARGA DURACION (1 AÑO):")
    print(token)
    print("========================================================")

if __name__ == "__main__":
    asyncio.run(generate_token())
