from json.decoder import JSONDecodeError
import requests
from requests.auth import HTTPBasicAuth
from root.logger import logs
import os
import json

filepath = "/req-files/departments.json"

def get_departments(count):
    if count % 100 == 0 or count == 1:
        api = os.environ["ANDREW_API"]
        departments = [] 
        temp_list = []
        page = 1

        while True:
            url = f"https://eastwest.freshservice.com/api/v2/departments?page={page}"
            response = requests.get(url, auth=HTTPBasicAuth(api, "X"))
            data = response.json()["departments"]
            if not data:
                break
            
            temp_list.append(data)
            page += 1     
       
        
        for temp_group in temp_list:
            for entry in temp_group:
                departments.append(entry)

        logs(f"Successfully loaded requested departments")

        save_departments(departments)

        return departments

    else:
        logs("Loading cached departments")
        departments = load_departments()

        return departments
    

def save_departments(departments):
    with open(filepath, "w") as file:
        json.dump(fp=file, obj=departments, indent=4) 

    logs("Succefully cached departments to departments.json")

def load_departments():
    try:
        with open(filepath, "r") as file:
            departments = json.load(file)

        logs("Successfylly loaded cached departments")
        return departments

    except FileNotFoundError:
        logs("Not able to load departments from cache, not able to find departments.json")
         
        return None

    except JSONDecodeError:
        logs("File departments.json empty, not able to load any departments")

        return None
