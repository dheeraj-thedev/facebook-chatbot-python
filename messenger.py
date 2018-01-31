import json
import requests

PAT = "" #Set this after you have linked your page to the app. You will get this more easily if you follow the tutorial.

def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"]

def send_message_with_id(PSID, text):
    """Send the message text to recipient with id recipient.
    """
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": PAT},
                      data=json.dumps({
            "recipient": {"id": PSID},
            "message": {"text": text}
        }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text


#To be used for customer matching purposes.
#The phone number, first name, and last name are all lazily matched in the sense that they do not need to be exact,
#just accurate enough that FB can search their database more easily.
#This is currently only valid for pages whose admins are US-based, but this can be used with phone numbers and customers across the world.
def send_message_with_phone_number(first_name, last_name, phone_number, message):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": PAT},
                      data=json.dumps({
                          "recipient": {"phone_number": phone_number, "first_name": first_name, "last_name": last_name},
                          "message": {"text": message}
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print r.text