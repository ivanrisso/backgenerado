
import sys
import os
import json
# Add project root to path
sys.path.append('/home/irisso/proyectos/facturacion')

try:
    from app.main import app
    from fastapi.routing import APIRoute
except ImportError as e:
    print(f"Error importing app: {e}")
    sys.exit(1)

def scan_backend():
    print("Scanning backend endpoints...")
    endpoints = []
    
    for route in app.routes:
        if isinstance(route, APIRoute):
            endpoints.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": route.name,
                "tags": route.tags,
                # Simple check for auth dependency in name or dependencies
                "auth_likely": "auth" in route.path or "login" in route.name or len(route.dependencies) > 0
            })
            
    output_path = '/home/irisso/proyectos/facturacion/.artifacts/requests/REQ-FUNC-004/backend/endpoints_data.json'
    with open(output_path, 'w') as f:
        json.dump(endpoints, f, indent=2)
        
    print(f"Scanned {len(endpoints)} endpoints.")

if __name__ == "__main__":
    scan_backend()
