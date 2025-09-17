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
from root.closed_tickets import write_closed_tickets, load_closed_tickets
from root.open_tickets import write_open_tickets, load_open_tickets
from root.used_tickets import write_used_tickets, load_used_tickets
from root.greeting import write_greeting_to_file
from root.logger import logs
from root.argparse import parse_args

def main():
    count = 1
    args = parse_args()
    dry_run = args.dry_run if args.dry_run else None

#dry run section
    if dry_run is True:
        logs("Dry running script")

        group_filtered_tickets = []

        old_open_tickets = load_open_tickets()
        tickets = get_tickets()
        departments = get_departments(count)

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
                    group_filtered(filtered_ticket, group_filtered_tickets)
                    print("\n")

        logs(f"{'Filtered ticket(s) end':=^40}")

        if old_open_tickets:
            for ticket in old_open_tickets:
                group_filtered_tickets.append(ticket)

        write_used_tickets(group_filtered_tickets)
        open_tickets, closed_tickets = check_down_tickets(group_filtered_tickets) 
        #need to add function that removes closed_tickets from group_filtered_tickets to allow for immediate removal of entry from script.
        write_open_tickets(open_tickets)
        write_closed_tickets(closed_tickets)

        script = ooo_script(group_filtered_tickets, closed_tickets)
        change = write_greeting_to_file(script)

        if change is True:
            token = get_bearer_token()
            logs(f"Would otherwise post '{script}' to email")
        else:
            logs("Skipping patching OOO due to no changes")

        group_filtered_tickets = None

        logs("End of python script dry run")
#dry run section ^

    else:
        try:
            while True:
                logs("Starting script")

                group_filtered_tickets = []

                old_open_tickets = load_open_tickets()
                tickets = get_tickets()
                departments = get_departments(count)

                logs(f"{'Filtered ticket(s) start':=^40}")

                if tickets:
                    for ticket in tickets:
                        filtered_ticket = filter_ticket(ticket)
                        if filtered_ticket:
                            post_ticket_note(filtered_ticket) 
                            components = get_service_components()
                            component_id = match_componenets(filtered_ticket, components)
                            post_to_status_page(filtered_ticket, component_id) 
                            match_department(filtered_ticket, departments)
                            set_fixed(filtered_ticket)
                            #priority(<json>) does fuzzy matching and from within priority() function, calles the set_priority() function passing the appropriate priority to set for that given ticket.
                            priority(filtered_ticket)
                            put_ticket_updates(filtered_ticket)
                            group_filtered(filtered_ticket, group_filtered_tickets)
                            print("\n")

                logs(f"{'Filtered ticket(s) end':=^40}")

                if old_open_tickets:
                    for ticket in old_open_tickets:
                        group_filtered_tickets.append(ticket)

                write_used_tickets(group_filtered_tickets)
                open_tickets, closed_tickets = check_down_tickets(group_filtered_tickets) 
                #need to add function that removes closed_tickets from group_filtered_tickets to allow for immediate removal of entry from script.
                write_open_tickets(open_tickets)
                write_closed_tickets(closed_tickets)

                script = ooo_script(group_filtered_tickets, closed_tickets)
                change = write_greeting_to_file(script)
                if change is True:
                    token = get_bearer_token()
                    patch_ooo(token, script)
                else:
                    logs("Skipping patching OOO due to no changes")

                group_filtered_tickets = None

                logs("End of python script, sleeping for 30 seconds.")

                count += 1
                ntime.sleep(30)

        except KeyboardInterrupt:
            print("\nStopping ISP down script")
