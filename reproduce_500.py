import requests
import json

def reproduce():
    url = "http://localhost:8000/api/v1/recibos/"
    
    # Payload based on the browser verification attempt
    payload = {
        "cliente_id": 4, # Adjust if needed
        "fecha_emision": "2026-02-04",
        "punto_venta": 1,
        "total": 100,
        "observaciones": "Reproduction Test",
        "imputaciones": []
    }
    
    # Need to get a token first? The browser failed with 500, implying auth worked but server crashed.
    # We'll assume we can use the 'newtester' if needed, or if we have a token.
    # The runbook says server allows skipping auth or we can login.
    # Let's try to login as admin just in case to eliminate auth issues, 
    # OR assume local dev environment might have open endpoints or we need to login.
    
    # Login as admin to get token
    login_url = "http://localhost:8000/api/v1/auth/login"
    login_data = {"username": "admin@example.com", "password": "admin123"} # Default credentials
    # Or use user from verification
    login_data_user = {"username": "newtester@gmail.com", "password": "tester123"}
    
    session = requests.Session()
    
    print("Logging in...")
    try:
        resp = session.post(login_url, data=login_data_user)
        if resp.status_code != 200:
            print("Login failed, trying admin...")
            resp = session.post(login_url, data=login_data)
        
        if resp.status_code == 200:
            token = resp.json()["access_token"]
            session.headers.update({"Authorization": f"Bearer {token}"})
            print("Login successful.")
        else:
            print(f"Login failed: {resp.text}")
            return
            
        print("Creating Recibo...")
        resp = session.post(url, json=payload)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    reproduce()
