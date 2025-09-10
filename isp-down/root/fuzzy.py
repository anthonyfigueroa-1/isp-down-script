from root.re import re_subject
from root.set_fields import set_department, set_priority
from root.api.tickets import post_private_note
from root.resub import normalize
from root.logger import logs

from polyfuzz import PolyFuzz

model = PolyFuzz("TF-IDF")

def match_componenets(ticket, componenets):
    comp_name_list = []
    down_site_name = re_subject(ticket)
    down_site_name = down_site_name.group(1)
    norm_down_site_name = []
    temp = normalize(down_site_name)
    norm_down_site_name.append(temp)

    for comp in componenets:
        if comp.get('name') and comp.get('id'):
            comp_name = normalize(comp.get('name'))
            comp_name_list.append([comp_name, comp.get('id')])

    comp_names = [t[0] for t in comp_name_list]

    model.match(norm_down_site_name, comp_names)

    df = model.get_matches()

    best_name = df.loc[0, "To"]
    similarity = df.loc[0, "Similarity"]

    logs(f"Match for {down_site_name} is {best_name} with a similarity score of {similarity}.")

    for comp in comp_name_list:
        if best_name in comp[0]:
            logs(f"Found the id of {comp[1]}, that is associated to {best_name}")
            return comp[1]

def match_department(ticket, departments):
    department_list = []
    down_list = []

    down_site = re_subject(ticket).group(1)
    norm_down_site = normalize(down_site)
    down_list.append(norm_down_site)

    for department in departments:
        if department.get("name", "") and department.get("id", ""):
            temp_name = normalize(department.get("name", ""))
            department_list.append([temp_name, department.get("id", "")])

    department_names = [d[0] for d in department_list] 

    model.match(down_list, department_names)

    df = model.get_matches()

    match = df.loc[0, "To"]
    similarity = df.loc[0, "Similarity"]

    logs(f"Set department for ticket #INC-{ticket.get('id')} to {match} with a score of {similarity}")

    if float(similarity) > 0.7:
        for department in department_list:
            if match in department[0]:
                set_department(ticket, department[1])
                #Need to add if to stop low similarity matches from going through
                logs(f"Found the id of {department[1]}, that is associated to {match}")
                return
    else:
        set_department(ticket, None)
        post_private_note(ticket, f"Could not find a good department match for {down_site}, please manually set department.")

def priority(ticket):
    site = []
    site_name = re_subject(ticket).group(1)
    site_name = normalize(site_name)
    site.append(site_name)

    urgent = []
    with open("/priority/urgent.txt", "r") as file:
        for line in file:
            line = normalize(line)
            urgent.append(line)

    model.match(site, urgent)

    df = model.get_matches()

    match = df.loc[0, "To"]
    similarity = df.loc[0, "Similarity"]

    if float(similarity) > 0.7 and match:
        set_priority(ticket, 4) 
        print(f"Setting ticket #INC-{ticket.get('id')} to 4")

    #If name contains EWH will set tickets to a priority of 3(high)
    elif "ewh" in site_name:
        set_priority(ticket, 3) 
        print(f"Setting ticket #INC-{ticket.get('id')} to 3")

    else:
        set_priority(ticket, 2) 
        print(f"Setting ticket #INC-{ticket.get('id')} to 2")
