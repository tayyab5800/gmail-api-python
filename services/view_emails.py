# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

class ViewEmails:

    def __init__(self) -> None:
        pass

    # utility functions
    def get_size_format(self, b, factor=1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"

    def parse_parts(self, service, parts, message):
        """
        Utility function that parses the content of an email partition
        """
        if parts:
            for part in parts:
                filename = part.get("filename")
                mimeType = part.get("mimeType")
                body = part.get("body")
                data = body.get("data")
                file_size = body.get("size")
                part_headers = part.get("headers")
                if part.get("parts"):
                    # recursively call this function when we see that a part
                    # has parts inside
                    self.parse_parts(service, part.get("parts"), message)
                if mimeType == "text/plain":
                    # if the email part is text plain
                    if data:
                        text = urlsafe_b64decode(data).decode()
                        print("Body:",text)
                else:
                    # attachment other than a plain text or HTML
                    for part_header in part_headers:
                        part_header_name = part_header.get("name")
                        part_header_value = part_header.get("value")
                        if part_header_name == "Content-Disposition":
                            if "attachment" in part_header_value:
                                # we get the attachment ID 
                                # and make another request to get the attachment itself
                                print("Found file:", filename, "size:", self.get_size_format(file_size))

    def show(self, service, message):
        """
        This function takes Gmail API `service` and the given `message_id` and does the following:
            - Prints email basic information (To, From, Subject & Date) and plain/text (Body) parts
        """
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        # parts can be the message body, or attachments
        payload = msg['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")
        if headers:
            # this section prints email basic info
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                if name.lower() == 'from':
                    # we print the From address
                    print("From:", value)
                elif name.lower() == "to":
                    # we print the To address
                    print("To:", value)
                elif name.lower() == "subject":
                    # make our boolean True, the email has "subject"
                    print("Subject:", value)
                elif name.lower() == "date":
                    # we print the date when the message was sent
                    print("Date:", value)
        # When attachements are available
        if parts:
            self.parse_parts(service, parts, message)
        else:
            body = payload.get("body")
            data = body.get("data")
            if data:
                    text = urlsafe_b64decode(data).decode()
                    print("Body:",text)
        print("="*50)
