import time as ntime

from root.api.tickets import get_tickets, put_ticket_updates, post_ticket_note, check_down_tickets 
from root.api.departments import get_departments
from root.api.status_page import post_to_status_page, get_service_components
from root.filter_ticket import filter_ticket
from root.set_fields import set_fixed
from root.fuzzy import match_componenets, match_department, priority
from root.api.ms_mail_token import get_bearer_token, patch_ooo
from root.group_filtered import group_filtered
from root.ooo_script import ooo_script
from root.greeting import write_greeting_to_file
from root.logger import logs
from root.argparse import parse_args
from root.sql.tickets import add_tickets_db, open_tickets_db, closed_tickets_db

def main():
    count = 1
    args = parse_args()
    dry_run = args.dry_run if args.dry_run else None

#dry run section
    if dry_run is True:
        logs("Dry running script")

        tickets = get_tickets()
        departments = get_departments(count)

        filtered_tickets = []

        logs(f"{'Filtered ticket(s) start':=^40}")

        if tickets:
            for ticket in tickets:
                filtered_ticket = filter_ticket(ticket)
                if filtered_ticket:
                    id = filtered_ticket.get('id')
                    logs(f"Would otherwise post ticket note for #INC-{id}")
                    components = get_service_components()
                    component_id = match_componenets(filtered_ticket, components)
                    logs(f"Would otherwise post ticket #INC-{id} to status page")
                    match_department(filtered_ticket, departments)
                    set_fixed(filtered_ticket)
                    #priority(<json>) does fuzzy matching and from within priority() function, calles the set_priority() function passing the appropriate priority to set for that given ticket.
                    priority(filtered_ticket)
                    logs(f"Would otherwise put ticket priority, status, categories, and tags to #INC-{id}")
                    filtered_tickets.append(filtered_ticket)
                if len(filtered_tickets) > 1:
                    logs(f"{'':=^40}")

        logs(f"{'Filtered ticket(s) end':=^40}")

        add_tickets_db(filtered_tickets)
        open_tickets = open_tickets_db()
        closed_tickets = check_down_tickets(open_tickets) 
        closed_tickets_db(closed_tickets)

        script = ooo_script(open_tickets)
        print(script)
        #change is a Boolean value
        change = write_greeting_to_file(script)

        if change is True:
            token = get_bearer_token()
            logs(f"Would otherwise post '{script}' to email")
        else:
            logs("Skipping patching OOO due to no changes")

        logs("End of python script dry run")
#dry run section ^

    else:
        try:
            while True:
                logs("Starting script")

                filtered_tickets = []

                tickets = get_tickets()
                departments = get_departments(count)

                logs(f"{'Filtered ticket(s) start':=^40}")

                if tickets:
                    for ticket in tickets:
                        filtered_ticket = filter_ticket(ticket)
                        if filtered_ticket:
                            id = filtered_ticket.get('id')
                            post_ticket_note(id) 
                            components = get_service_components()
                            component_id = match_componenets(filtered_ticket, components)
                            post_to_status_page(filtered_ticket, component_id) 
                            match_department(filtered_ticket, departments)
                            set_fixed(filtered_ticket)
                            #priority(<json>) does fuzzy matching and from within priority() function, calles the set_priority() function passing the appropriate priority to set for that given ticket.
                            priority(filtered_ticket)
                            put_ticket_updates(filtered_ticket)
                            filtered_tickets.append(filtered_ticket)
                        if len(filtered_tickets) > 1:
                            logs(f"{'':=^40}")

                logs(f"{'Filtered ticket(s) end':=^40}")

                add_tickets_db(filtered_tickets)
                open_tickets = open_tickets_db()
                closed_tickets = check_down_tickets(open_tickets) 
                closed_tickets_db(closed_tickets)

                script = ooo_script(open_tickets)
                #change is a Boolean value
                change = write_greeting_to_file(script)                

                if change is True:
                    token = get_bearer_token()
                    patch_ooo(token, script)
                else:
                    logs("Skipping patching OOO due to no changes")

                logs("End of python script, sleeping for 30 seconds.")

                count += 1
                ntime.sleep(30)

        except KeyboardInterrupt:
            print("\nStopping ISP down script")
