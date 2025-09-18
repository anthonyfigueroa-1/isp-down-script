from root.re import re_subject
from root.logger import logs
from root.sql.tickets import query_tickets_db

def filter_ticket(ticket):
    site_name = re_subject(ticket)
    id = ticket.get("id")
    status = ticket.get("status")
    ticket_in_db = False

    t = query_tickets_db(id)
    if t:
        ticket_in_db = True

    if (site_name) and (status in (2, 3)) and (ticket_in_db is False):
            logs(f"Ticket passed filters: #INC-{ticket.get('id')}")
            return ticket

    else:
        return
