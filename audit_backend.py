import asyncio
import httpx
import sys
import os
from fastapi import FastAPI
from fastapi.routing import APIRoute

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.main import app

def list_routes():
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            methods = list(route.methods)
            for method in methods:
                routes.append({
                    "path": route.path,
                    "method": method,
                    "name": route.name,
                    "tags": route.tags
                })
    return routes

async def verify_get_endpoints(routes):
    results = {}
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=10) as client:
        for r in routes:
            if r["method"] == "GET" and "{" not in r["path"]:
                try:
                    print(f"Checking {r['path']} ...", end="", flush=True)
                    response = await client.get(r["path"])
                    print(f" {response.status_code}")
                    results[r["path"]] = response.status_code
                except Exception as e:
                    print(f" ERROR: {e}")
                    results[r["path"]] = "ERROR"
    return results

if __name__ == "__main__":
    print("--- API INVENTORY ---")
    all_routes = list_routes()
    for r in sorted(all_routes, key=lambda x: x["path"]):
        print(f"{r['method']} {r['path']} [{', '.join(r['tags'])}]")
    
    print("\n--- SMOKE TEST (GET LISTs) ---")
    asyncio.run(verify_get_endpoints(all_routes))
