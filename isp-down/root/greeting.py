import os
from root.logger import logs

path = "/message/greeting.txt"

def write_greeting_to_file(script):

    with open(path, "r") as file:
        test = file.read()

    if test == '':
        test = None
    
    if test == script:
        logs("No changes, leaving greeting.txt as it was.")
        return False

    if not script:
        with open(path, "w") as file:
            pass
        logs("No script to write, clearing file contents for greeting.txt") 
        return True

    with open(path, "w") as file:
        file.write(script)

    logs("Wrote greeting to greeting.txt")

    return True
