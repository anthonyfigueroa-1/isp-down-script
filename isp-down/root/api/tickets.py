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

def post_ticket_note(id):

    url = f"https://eastwest.freshservice.com/api/v2/tickets/{id}/notes"
    payload = {
            "private": True,
            "body": "Please use this article to troubleshoot and resolve this ticket if you need help:<br><br><a href='https://support.eastwestcloud.com/a/solutions/articles/5000093284' target='_blank' rel='noopener norefferer'><b>Network Outage: 'ISP is Down' Resolution & Fresh Service Status Page Updates</b></a>"
            }

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

def post_private_note(id, string):
    url = f"https://eastwest.freshservice.com/api/v2/tickets/{id}/notes"

    payload = {
            "body": string,
            "private": True
            }
    

    response = requests.post(url, json=payload, auth=HTTPBasicAuth(api, "X"))

    logs(f"Response status code for request to POST '{string}' is {response.status_code}")

def check_down_tickets(isp_tickets):
    if not isp_tickets:
        return None

    closed_tickets = []
    open_tickets = []

    header = {
            "Content-Type": "application/json"
            }

    for ticket_id in isp_tickets:
        url = f"https://eastwest.freshservice.com/api/v2/tickets/{ticket_id}"

        response = requests.get(url, headers=header, auth=HTTPBasicAuth(api, "X"))

        t = response.json()["ticket"]

        id = t.get('id')
        status = t.get('status')

        match status:
            case 2:
                open_tickets.append(id)

            case 3:
                open_tickets.append(id)

            case 4:
                closed_tickets.append(id)
                logs(f"Status for #INC-{id} is (RESOLVED). Marking ticket as closed in database.")

            case 5:
                closed_tickets.append(id)
                logs(f"Status for #INC-{id} is (CLOSED). Marking ticket as closed in database.")

            case _:
                continue

    isp_tickets = open_tickets
    return closed_tickets
