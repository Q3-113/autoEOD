import requests 
from datetime import datetime

workspace_id = "" # Toggl workspace id
api_token = "" # Toggl API token
user = "" # Toggl user name

base_url = "https://api.track.toggl.com/reports/api/v2/details"
user_agent = "autoEOD"
date = datetime.today().isoformat()

auth = (api_token, "api_token")

payload = {
    "user_agent": user_agent,
    "workspace_id": workspace_id,
    "since": date
}

r = requests.get(base_url, auth=auth, params=payload)
r.raise_for_status()

events = r.json()["data"]
projects = set()
events_by_project = {}

for e in events:
    p = e["project"]
    event = e["description"]

    if not e["user"] == user:
        continue

    projects.add(p)

    if not p in events_by_project:
        events_by_project[p] = [event]
    else:
        events_by_project[p].insert(0, event)
    
for p in projects:
    print(p + "\nEOD: " + ", ".join(e for e in events_by_project[p]) + "\n")
