from root.logger import logs

path = "/message/greeting.txt"

def write_greeting_to_file(script):

    try:
        with open(path, "r") as file:
            temp = file.read()

        if temp == '':
            temp = None
        
        if temp == script:
            logs("No changes, leaving greeting.txt as it was.")
            return False

    except FileNotFoundError:
        logs("greeting.txt file not found, no script to write.")
        logs("Creating empty greeting.txt file.")
        with open(path, "w") as file:
            pass

    if not script:
        with open(path, "w") as file:
            pass
        logs("No script to write, clearing file contents for greeting.txt") 
        return True

    with open(path, "w") as file:
        file.write(script)

    logs("Wrote greeting to greeting.txt")

    return True
