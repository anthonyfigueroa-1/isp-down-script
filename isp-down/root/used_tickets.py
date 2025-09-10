from root.logger import logs

def write_used_tickets(tickets):
    if not tickets:
        logs("No new used tickets to write to used_tickets.txt")
        return
    with open("/req-files/used_tickets.txt", "w") as f:
        for ticket in tickets:
            id = ticket.get("id")
            f.write(f"{id} " + "\n")
    logs("Writing to used_tickets.txt")

def load_used_tickets():
    #No logs due to this being loaded within the for loop for filtered tickets
    used_tickets_list = []
    
    try:
        with open("/req-files/used_tickets.txt", "r") as f:
            for line in f:
                used_tickets_list.append(line)
    except FileNotFoundError:
        return

    return used_tickets_list
