from root.logger import logs

def write_closed_tickets(tickets):
    append_list = []
    if not tickets:
        return
    with open("/req-files/closed_tickets.txt", "a") as f:
        for ticket in tickets:
            id = ticket.get("id")
            append_list.append(str(id))
            f.write(f"{id} " + "\n")

    if len(append_list) == 1:            
        logs(f"Appended ticket {append_list[0]} to closed_tickets.txt")
    elif len(append_list) >= 2:
        logs(f"Appended tickets {', '.join(append_list)} to closed_tickets.txt")
    else:
        logs(f"Somethings went wrong when checking the length of list for tickets being written to closed_tickets.txt")


def load_closed_tickets():
    #No logs due to this being loaded within the for loop for filtered tickets
    closed_tickets_list = []
    
    try:
        with open("/req-files/closed_tickets.txt", "r") as f:
            for line in f:
                closed_tickets_list.append(line)
    except FileNotFoundError:
        return

    return closed_tickets_list
