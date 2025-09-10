import requests
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime, timezone, timedelta

from root.re import re_subject
from root.logger import logs

api = os.environ["ANDREW_API"]

def get_service_components():
    url = "https://eastwest.freshservice.com/api/v2/status/pages/1724/service-components"

    response = requests.get(url, auth=HTTPBasicAuth(api, "X"))

    logs(f"Get service components status code: {response.status_code}")

    info = response.json()["service_components"]

    components = [{}]

    for location in info:
        for site in location["components"]:
            for t in site["components"]:
                components.append({"name": t.get('name', ''), "id": t.get('id', '')})

    return components

def post_to_status_page(ticket, component_id):
    url = f"https://eastwest.freshservice.com/api/v2/tickets/{ticket.get('id')}/status/pages/1724/incidents"
    offset = timezone(timedelta(hours=6, minutes=0))
    now = datetime.now(offset)
    formatted = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    formatted = formatted[:-2] + ":" + formatted[-2:]
    site_name = re_subject(ticket)
    headers = {
            "Content-Type": "application/json"
            }
    payload = {
            "title":f"Site {str(site_name.group(1))} is currently down",
            "description": f"We are aware and looking into the cause of {str(site_name.group(1))} being down.",
            "started_at": formatted,
            "impacted_services": [
                {
                    "id": component_id,
                    "status": 30
                }
                ]
            }

    response = requests.post(url ,headers=headers, json=payload, auth=HTTPBasicAuth(api, "X"))
    
    logs(f"Post to status page status code: {response.status_code}")
