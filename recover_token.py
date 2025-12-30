
import time
import logging
from datetime import datetime, timedelta
from app.core.afip.wsaa import WSAAClient
from app.core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recover():
    # Target time: 2025-12-27T16:46:44-03:00
    # Unix timestamp calculation
    # Hand-calculate or use datetime
    
    # Range: 16:46:00 to 16:55:00 (cover until recent attempts just in case)
    # Actually, the "Valid TA" is the FIRST one generated that hasn't expired.
    # So we should look around 16:46:44.
    
    target_date = datetime(2025, 12, 27, 16, 46, 0) # Local time approx?
    # Note: time.time() is UTC? No, unix timestamp is independent of zone, but it's seconds since epoch UTC.
    # The server time is provided in metadata: "2025-12-27T16:46:44-03:00"
    # So I need to convert that to timestamp.
    
    # 16:46:44 -03:00 is 19:46:44 UTC.
    
    start_dt = datetime(2025, 12, 27, 19, 45, 0) # UTC
    end_dt =   datetime(2025, 12, 27, 19, 58, 0) # UTC
    
    start_ts = int(start_dt.timestamp())
    end_ts = int(end_dt.timestamp())
    
    logger.info(f"Scanning timestamps from {start_ts} to {end_ts} (Range: {end_ts - start_ts} seconds)")

    wsaa = WSAAClient(
        key_path=settings.AFIP_KEY_CRT_PATH if settings.AFIP_KEY_CRT_PATH else "app/certificado/clave",
        cert_path=settings.AFIP_CERT_CRT_PATH if settings.AFIP_CERT_CRT_PATH else "app/certificado/group.crt",
        production=settings.AFIP_ENVIRONMENT.lower() == "production"
    )
    
    # Hack _create_tra to accept unique_id
    original_create_tra = wsaa._create_tra
    for uid in range(start_ts, end_ts + 1):
        if uid % 50 == 0:
            print(f"Trying uid {uid}...", end="\r")
            
        def mock_create_tra():
            # Try to send the OLD uniqueId (uid) but with NEW timestamps (now)
            # This hopes that AFIP checks uniqueId collision FIRST and returns cache,
            # ignoring that the timestamp in the content differs from the original request.
            # If AFIP parses the uniqueId, sees it exists, and returns the token, we win.
            
            gen_now = datetime.now() - timedelta(minutes=2)
            exp_now = gen_now + timedelta(minutes=20)
            fmt = "%Y-%m-%dT%H:%M:%S"
            
            # Use the OLD uid
            xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<loginTicketRequest version="1.0">
  <header>
    <uniqueId>{uid}</uniqueId>
    <generationTime>{gen_now.strftime(fmt)}-03:00</generationTime>
    <expirationTime>{exp_now.strftime(fmt)}-03:00</expirationTime>
  </header>
  <service>{wsaa.service}</service>
</loginTicketRequest>"""
            return xml

        wsaa._create_tra = mock_create_tra
        
        try:
            tra = wsaa._create_tra()
            cms = wsaa._sign_tra(tra)
            token, sign, exp = wsaa._call_wsaa(cms)
            
            logger.info(f"\n\nSUCCESS! RECOVERED TOKEN for UID {uid}")
            # ... save ...
            wsaa._token = token
            wsaa._sign = sign
            wsaa._expiration = exp
            wsaa._save_to_cache()
            print("Token Recovered and Saved!")
            return
            
        except Exception as e:
             # If "CEE ya posee", it means uniqueId logic treated this as NEW request (so ID didn't match old cache key)
             # If "CMS... invalido", signature mismatch (expected).
             # If "Success", we win.
             msg = str(e)
             if "El CEE ya posee" not in msg:
                 # Interesting error?
                 if "formato o dato" in msg:
                    pass
                 else:
                    # logger.info(f"{uid}: {msg}")
                    pass

if __name__ == "__main__":
    recover()
