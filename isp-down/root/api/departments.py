import requests
from requests.auth import HTTPBasicAuth
from root.logger import logs
from root.sql.departments import add_dep_db, load_dep_db
import os

filepath = "/req-files/departments.json"

def get_departments(count):
    if count % 500 == 0 or count == 1:
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

        departments = load_dep_db()

        return departments

    else:
        logs("Loading cached departments")
        departments = load_departments()

        return departments
    

def save_departments(departments):
    add_dep_db(departments)

    logs("Succefully cached departments to departments.db")

def load_departments():

    departments = load_dep_db()

    logs("Successfylly loaded cached departments")

    return departments


