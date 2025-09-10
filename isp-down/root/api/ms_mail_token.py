import msal
import requests
import os
from root.logger import logs

def get_bearer_token():
    #The AZ App ID
    client_id = os.environ["MAIL_CLIENT"]
    #The login URL for our tenant
    tenant_id = os.environ["MAIL_TENANT"]
    #A secure key
    mail_secret = os.environ["MAIL_SECRET"]

    #To let MS know which, e.g. EastWest, is the tenant I am attempting to access.
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    #.default grants me access to all settings, limited to the settings stated when creating AZ AD App.
    scope = ["https://graph.microsoft.com/.default"]
    #Let's me access users and final /{property} allows me to state what I want access to.
    graph_url = "https://graph.microsoft.com/v1.0/users/support@eastwestcloud.com/mailboxSettings"

    logs(f"Attempting to get bearer token from Microsoft") 
    
    #Uses the above to create an authenticationclient that represenets this script when using client credentials flow, a flow used for automated apps.
    app = msal.ConfidentialClientApplication(
            client_id=client_id,
            authority=authority,
            client_credential=mail_secret
            )
    #Uses app object to request access for token from MS, returning bearer token.
    token_response = app.acquire_token_for_client(scopes=scope)

    if "access_token" in token_response:
        token = token_response.get("access_token")
        logs("Bearer token acquired from Microsoft")
        return token
    else:
        logs("Failed to get bearer token from Microsoft")

        
def patch_ooo(token, script):
    graph_url = "https://graph.microsoft.com/v1.0/users/support@eastwestcloud.com/mailboxSettings"

    header = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
            }        

    if not script:
        payload = {
                "automaticRepliesSetting": {
                    "status": "disabled"
                    }
                }
        response = requests.patch(graph_url, json=payload, headers=header)

        logs(f"OOO response code: {response.status_code}")
        logs("No sites down, removing OOO status and message")

        return False

    payload = {
            "automaticRepliesSetting": {
                "status": "alwaysEnabled",
                "externalAudience": "all",
                "internalReplyMessage": script
                }
            }
    response = requests.patch(graph_url, json=payload, headers=header)

    logs(f"OOO response code: {response.status_code}")
    logs(f"OOO message updated to '{script}'")

    return False 
