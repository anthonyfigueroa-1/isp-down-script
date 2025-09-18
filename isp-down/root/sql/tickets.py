import sqlite3
import json

from root.logger import logs

file = "/req-files/db/tickets.db"

def create_tickets_db():
    db = sqlite3.connect(file)

    cursor = db.cursor()

    #Checks to make sure db(database) file exists, if not makes it
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS tickets
                   (
                       ticket_id NUM PRIMARY KEY,
                       ninja_id NUM,
                       closed NUM,
                       json TEXT
                       )
                   """)
    db.commit()

    cursor.close()
    db.close()

#passing group_filtered_tickets here
def add_tickets_db(tickets):
    db = sqlite3.connect(file)

    cursor = db.cursor()

    cursor.execute("""
                   ATTACH DATABASE tickets AS tickets
                   """)

    for ticket in tickets:
        try:
            cursor.execute("""
                           INSERT INTO tickets (ticket_id, closed, json)
                           VALUES(?, ?, ?)""",
                           (ticket.get("id"), False, json.dumps(ticket)))
            db.commit()
            logs(f"Added ticket #INC-{ticket.get('id')} to tickets.db")

        except sqlite3.IntegrityError:
            logs(f"Ticket #INC-{ticket.get('id')} already in tickets.db")

    cursor.close()
    db.close()

def open_tickets_db():
    db = sqlite3.connect(file)
    cursor = db.cursor()

    cursor.execute("""
                   ATTACH DATABASE tickets AS tickets
                   """)

    cursor.execute("SELECT ticket_id FROM tickets WHERE closed = False")
    tickets = cursor.fetchmany()

    open_tickets = []

    cursor.close()
    db.close()

    for ticket in tickets:
        open_tickets.append(ticket[0])

    return open_tickets

def closed_tickets_db(closed_tickets):
    if not closed_tickets:
        return

    db = sqlite3.connect(file)
    cursor = db.cursor()

    cursor.execute("""
                   ATTACH DATABASE tickets AS tickets
                   """)

    for ticket in closed_tickets:
        cursor.execute("UPDATE tickets SET closed = True WHERE ticket_id = ? AND closed = False", (ticket,))
        db.commit()

    cursor.close()
    db.close()

def query_tickets_db(ticket_id):
    db = sqlite3.connect(file)

    cursor = db.cursor()

    cursor.execute("""
                   ATTACH DATABASE tickets AS tickets
                   """)

    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    ticket = cursor.fetchone()

    cursor.close()
    db.close()

    return ticket
