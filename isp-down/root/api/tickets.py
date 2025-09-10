from requests.auth import HTTPBasicAuth
from root.logger import logs
import requests
import os
from time import sleep

api = os.environ["ANTHONY_API"]

def get_tickets():
    url = "https://eastwest.freshservice.com/api/v2/tickets"
    response = requests.get(url, auth=HTTPBasicAuth(api, "X"))
    logs(f"Reponse status code for request to GET tickets is {response.status_code}")

    tickets = response.json()['tickets']
    
    return tickets

def post_ticket_note(ticket):
    if not ticket:
        return

    ticket_id = ticket.get("id", None)

    url = f"https://eastwest.freshservice.com/api/v2/tickets/{ticket_id}/notes"
    payload = {
            "private": True,
            "body": "Please use this article to troubleshoot and resolve this ticket if you need help:<br><br><a href='https://support.eastwestcloud.com/a/solutions/articles/5000093284' target='_blank' rel='noopener norefferer'><b>Network Outage: 'ISP is Down' Resolution & Fresh Service Status Page Updates</b></a>"
            }

    if ticket_id:
        response = requests.post(url, json=payload, auth=HTTPBasicAuth(api, "X"))

        logs(f"Response status code for request to POST private note about solutions article is {response.status_code}")

def put_ticket_updates(ticket):
    url = f"https://eastwest.freshservice.com/api/v2/tickets/{ticket.get('id')}"

    payload = {
            "priority": ticket.get("priority"),
            "department_id": ticket.get("department_id"),
            "custom_fields":{
                    "issues_category": ticket.get("category"),
                    "sub_category_1": ticket.get("sub_category"),

                },
                    "tags": ticket.get("tags")
               }

    response = requests.put(url, json=payload, auth=HTTPBasicAuth(api, "X"))

    logs(f"Response status code for request to PUT ticket fields is {response.status_code}")

def post_private_note(ticket, string):
    url = f"https://eastwest.freshservice.com/api/v2/tickets/{ticket.get('id')}/notes"

    payload = {
            "body": string,
            "private": True
            }
    

    response = requests.post(url, json=payload, auth=HTTPBasicAuth(api, "X"))

    logs(f"Response status code for request to POST '{string}' is {response.status_code}")

def check_down_tickets(isp_tickets):
    if not isp_tickets:
        return None, None

    open_tickets = []
    closed_tickets = []

    header = {
            "Content-Type": "application/json"
            }

    for ticket in isp_tickets:

        url = f"https://eastwest.freshservice.com/api/v2/tickets/{ticket.get('id')}"

        response = requests.get(url, headers=header, auth=HTTPBasicAuth(api, "X"))

        t = response.json()["ticket"]

        id = ticket.get('id')
        status = ticket.get('status')

        match status:
            case 2:
                open_tickets.append(t)
                logs(f"Status for #INC-{id} is ({status}). Adding ticket to open_tickets.json.")

            case 3:
                open_tickets.append(t)
                logs(f"Status for #INC-{id} is ({status}). Adding ticket to open_tickets.json.")

            case 4:
                closed_tickets.append(t)
                logs(f"Status for #INC-{id} is ({status}). Adding ticket id to closed_tickets.txt.")

            case 5:
                closed_tickets.append(t)
                logs(f"Status for #INC-{id} is ({status}). Adding ticket id to closed_tickets.txt.")

            case _:
                logs(f"Could not find valid status for #INC-{id}. Skipping ticket in function root.api.tickets.isp_tickets")
                continue 

    return open_tickets, closed_tickets
