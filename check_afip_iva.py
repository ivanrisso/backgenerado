
import asyncio
from app.core.afip_client import get_afip_client

async def check_afip():
    client = get_afip_client() # WSFEClient
    # Check if we can call FEParamGetTiposIva
    # Need to see how WSFEClient exposes this. 
    # If not exposed directly, we access client.client.service explicitly?
    # WSFEClient uses Zeep.
    
    # Actually WSFEClient might not expose get_param_tipos_iva directly yet.
    # Let's use the internal client.
    
    try:
        # Assuming get_afip_client connects and authenticates on demand
        print("Authenticating with AFIP...")
        token, sign = client.wsaa_client.get_token_and_sign()
        
        from zeep import Client
        wsfe_client = Client(client.wsdl) 
        
        auth = {
            "Token": token,
            "Sign": sign,
            "Cuit": client.cuit
        }
        
        print("Calling FEParamGetTiposIva...")
        response = wsfe_client.service.FEParamGetTiposIva(Auth=auth)
        
        # Parse response
        # Structure: ResultGet -> IvaTipo -> [ { Id, Desc, FchDesde, FchHasta }, ... ]
        
        print("\n--- DATOS OFICIALES AFIP (FEParamGetTiposIva) ---")
        if response.ResultGet and response.ResultGet.IvaTipo:
            for item in response.ResultGet.IvaTipo:
                print(f"ID: {item.Id:<5} | Desc: {item.Desc}")
        else:
            print("No se obtuvieron datos o estructura inesperada.")
            print(response)

    except Exception as e:
        print(f"Error checking AFIP: {e}")

if __name__ == "__main__":
    asyncio.run(check_afip())
