import re

def re_subject(ticket):
    return re.search(r"Alert - Network Devices -\s([^\-]+)\s\w+\s\(.+\)", ticket.get('subject'))
