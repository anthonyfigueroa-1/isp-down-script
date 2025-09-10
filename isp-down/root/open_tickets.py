import json
from json.decoder import JSONDecodeError 
from root.logger import logs

def write_open_tickets(tickets):
    if not tickets:
        with open("/req-files/open_tickets.json", "w") as f:
            pass
        return

    with open("/req-files/open_tickets.json", "w") as f:
       json.dump(tickets, f) 
    
    logs("Wrote open_tickets to file open_tickets.json")

def load_open_tickets():
    try:
        with open("/req-files/open_tickets.json", "r") as f:
            group_filtered_tickets = json.load(f)

    except FileNotFoundError:
        logs("Was not able to find open_tickets.json in file open_tickets.json")
        return
    except JSONDecodeError:
        logs("No open tickets found in open_tickets.json")
        return

    logs("Loading open ticket(s) found in open_tickets.json")

    return group_filtered_tickets
