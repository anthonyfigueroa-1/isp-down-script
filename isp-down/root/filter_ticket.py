import re
from root.re import re_subject
from root.closed_tickets import load_closed_tickets
from root.used_tickets import load_used_tickets
from root.logger import logs

def filter_ticket(ticket):
    id = ticket.get('id')
    site_name = re_subject(ticket)

    closed_tickets = load_closed_tickets()
    closed_tickets_string = f"{closed_tickets}"
    closed_match = re.search(rf"({id})", closed_tickets_string)

    used_tickets = load_used_tickets()
    used_tickets_string = f"{used_tickets}"
    used_match = re.search(rf"({id})", used_tickets_string)

    if not site_name:
        return None

    if (site_name) and (ticket.get("status", None) is None or ticket.get("status") == 2 or 3) and (used_match is None) and (closed_match is None):
        logs(f"Ticket passed filters: #INC-{ticket.get('id')}")
        return ticket
