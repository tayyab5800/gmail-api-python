# Initital Setup
1. Install Python 3.10+
2. Create Test Gmail Account
3. Create Cloud Project
4. Enable Gmail API
5. Authorize credentials for a desktop application
6. Conifure Consent Screen (For first time user) -> In OAuth consent screen (Select External option in User Type) 
    -> Add Scope -> Add Test User
7. Create and download JSON Credential file (for Desktop App)
8. Download quickstart.py and verify app access. (One Time)

# Main Code
9. Run gmailapi.py file to see the results. (gmail_authenticator() will verify the user authentication.)
10. After running whole code you will see how many times your given keyword is found in test gmail account.
11. Basic info will be shown in the terminal e.g(To, From, Subject, Date, Body, Attachment Name and Size (if any!!!)).
12. Un-comment Sender.send_message() to send a message and you will see addition in to the viewing email results.