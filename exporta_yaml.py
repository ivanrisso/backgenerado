# export_openapi_yaml.py
import requests
import yaml

# Cambiá si tu app no está en localhost:8000
response = requests.get("http://localhost:8000/openapi.json")
data = response.json()

with open("openapi.yaml", "w") as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True)

print("✅ Exportado como openapi.yaml")
