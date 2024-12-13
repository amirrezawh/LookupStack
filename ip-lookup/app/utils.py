import requests
import json
from fastapi import HTTPException

def fetch_region_from_api(ip_address: str) -> str:
    api_url = f"https://geolocation-db.com/jsonp/{ip_address}"
    response = requests.get(api_url)
    if response.status_code == 200:
        output = response.text
        start_idx = output.find('{')
        end_idx = output.rfind('}') + 1
        json_string = output[start_idx:end_idx]
        data = json.loads(json_string)
        return data.get("country_name", "Unknown")
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch region from external API")

