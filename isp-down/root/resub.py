import re

acs = {
    "ns": "northstar",
    "og": "old greenwood",
    "sbv": "snowmass base village",
    "bc": "beaver creek",
    "bg": "bachelor gulch"
}

remove_non_text = re.compile(r"[^\w\s]+")

def normalize(script):

    t = script.lower().strip()

    t = remove_non_text.sub(" ", t)

    t = re.sub(r"\s+", " ", t)

    words = [acs.get(w, w) for w in t.split()]

    return ' '.join(words)
