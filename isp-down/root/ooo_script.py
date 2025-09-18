from root.re import re_subject
from root.logger import logs
from root.sql.tickets import query_tickets_db
import json

def ooo_script(open_tickets):
    if not open_tickets:
        return None
    
    site_name_list = []

    for ticket in open_tickets:
        ticket = query_tickets_db(ticket)
        ticket = json.loads(ticket[3])
        site_name = re_subject(ticket).group(1)
        site_name_list.append(site_name)

    if len(site_name_list) == 2:
        return f"We are aware that {' and '.join(site_name_list)} are down and we are currently working on resolving the issue."

    elif len(site_name_list) == 1:
        return f"We are aware that {site_name_list[0]} is down and we are currently working on resolving the issue."

    else:
        return f"We are aware that {', '.join(site_name_list)} are down and we are currently working on resolving the issue."
