from root.logger import logs

def set_department(ticket, department_id):
    ticket["department_id"] = department_id

def set_fixed(ticket):
    set_categories(ticket)
    set_tags(ticket)
    logs(f"Set categories and tags to ticket #INC-{ticket.get('id')}")

def set_priority(ticket, num):
    ticket["priority"] = num

def set_categories(ticket):
    ticket["category"] = "Network"
    ticket["sub_category"] = "Troubleshooting"

def set_tags(ticket):
    ticket["tags"] = ["ISP", "T1"]

def set_status_page_id(ticket, status_page_id):
    ticket["status_page_incident_id"] = status_page_id
    logs(f"Set status_page_id for ticket #INC-{ticket.get('id')} to {status_page_id}")
