from services.gmail_authenticator import GmailAuthenticator
from services.sender import Sender
from services.view_emails import ViewEmails

def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

# get the Gmail API service
auth = GmailAuthenticator()
service = auth.verify()

# test send email (Service Obj, To, Subject, Body, Attachement)
# Un-comment to send a message and and you will see addition in to the viewing email result
'''sender = Sender()
sender.send_message(service, "tayyab5800@gmail.com", "Gmail API Subject Tesing", 
            "Gmail API Body testing of the email. haensel ###", ["Readme.md"])'''

# get emails that match the query you specify search_messages(SERVICE, KEYWORD)
results = search_messages(service, "haensel")
print(f"Found {len(results)} results.")

email_viewer = ViewEmails()
# for each email matched, read it (output plain/text and attachement to console)
for msg in results:
    email_viewer.show(service, msg)