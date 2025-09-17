import sqlite3
import json

from root.logger import logs

#passing filtered_tickets here
def add_tickets_db(tickets):
    db = sqlite3.connect("/db/tickets.db")

    cursor = db.cursor()

#Checks to make sure db(database) file exists, if not makes it
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS tickets
                   (
                       ticket_id NUM PRIMARY KEY,
                       ninja_id NUM,
                       json TEXT
                       )
                   """)
    db.commit()

    for ticket in tickets:
        try:
            cursor.execute("""
                           INSERT INTO tickets (ticket_id, json)
                           VALUES(?, ?)""",
                           (ticket.get("id"), json.dumps(ticket)))
            db.commit()
            logs(f"Added ticket #INC-{ticket.get('id')} to tickets.db")

        except sqlite3.IntegrityError:
            logs(f"Ticket #INC-{ticket.get('id')} already in tickets.db")

    cursor.close()
    db.close()

#Passing closed/resolved ticket ID's here
def remove_tickets_db(tickets):
    db = sqlite3.connect("/db/tickets.db")

    cursor = db.cursor()

    cursor.execute("""
                   ATTACH tickets DATABASE AS tickets
                   """)

    for id in tickets:
        cursor.execute("""
                       DELETE FROM tickets
                       WHERE ticket_id IS ?
                       """,
                       (id,))
        db.commit()

    cursor.close()

    db.close()

def load_tickets_db():
    db = sqlite3.connect("/db/tickets/db")

    cursor = db.cursor()

    cursor.execute("""
                   ATTACH tickets DATABASE AS tickets
                   """)

    cursor.execute("SELECT json FROM tickets")
    #can only grab info in tuples so will need to extract and append to seperate list
    ticket_tup = cursor.fetchall()

    cursor.close()
    db.close()

    tickets = []

    for ticket in ticket_tup:
        jsn = json.loads(ticket[0])
        tickets.append(jsn)

    return tickets
