import httpx
import asyncio

async def test_api():
    base_url = "http://localhost:8000/api/v1"
    
    # Login
    async with httpx.AsyncClient(base_url=base_url) as client:
        print("Logging in...")
        response = await client.post("/auth/login", json={
            "usuario_email": "admin@facturacion.local",
            "usuario_password": "admin.password.dev"
        })
        
        if response.status_code != 200:
            print(f"Login failed: {response.status_code} {response.text}")
            return

        print("Login successful. Cookies:", client.cookies)

        # 1. Test /usuarios (Known Good)
        print("\nTesting /usuarios/ ...")
        resp_users = await client.get("/usuarios/")
        print(f"Status: {resp_users.status_code}")
        if resp_users.status_code != 200:
            print(f"Response: {resp_users.text}")

        # 2. Test /clientes/ (Known Bad)
        print("\nTesting /clientes/ ...")
        resp_clientes = await client.get("/clientes/")
        print(f"Status: {resp_clientes.status_code}")
        if resp_clientes.status_code != 200:
            print(f"Response: {resp_clientes.text}")

if __name__ == "__main__":
    asyncio.run(test_api())
