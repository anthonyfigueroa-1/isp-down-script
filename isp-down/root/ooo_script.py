from root.re import re_subject
from root.logger import logs

def ooo_script(filtered_tickets, closed_tickets):
    if not filtered_tickets:
        return None
    
    site_name_list = []
    ticket_count = 0

    closed = False

    for ticket in filtered_tickets:
        site_name = re_subject(ticket).group(1)
        #check if ticket is in closed_tickets list
        for closed_t in closed_tickets:
            if ticket.get('id') == closed_t.get('id'):
                logs(f'Ticket #INC-{ticket.get("id")} found in closed and not adding to OOO SCRIPT')
                closed = True
        if site_name not in site_name_list and closed == False:
            site_name_list.append(site_name)
            ticket_count += 1

    if ticket_count == 2:
        return f"We are aware that {' and '.join(site_name_list)} are down and we are currently working on resolving the issue."

    elif ticket_count == 1:
        return f"We are aware that {site_name_list[0]} is down and we are currently working on resolving the issue."

    elif ticket_count == 1 and closed == True:
        return None

    return f"We are aware that {', '.join(site_name_list)} are down and we are currently working on resolving the issue."
