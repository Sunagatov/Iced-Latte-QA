import email
import email.utils
import email.utils
import imaplib
import re
import time
from typing import Union


class Email:
    def __init__(self, imap_server: str, email_address: str, gmail_password: str):
        self.imap_server = imap_server
        self.email_address = email_address
        self.password = gmail_password

    def extract_confirmation_code_from_email(self, email_box: str, key: str, value: str) -> Union[str, None]:
        """ Method for  extraction confirmation code  for registration from user's email

        Args:
            email_box: email's folder, where search is performs
            key: criterion to search message through email
                 Examples: "FROM"
            value: criterion to search message through email
                   Examples: "email.email@gmail.com"
        """
        attempt = 0
        delay = 10
        max_attempts = 3
        while attempt < max_attempts:
            current_time = time.time()
            # establish connect to the email server, select folder to perform search in and
            # search email message by specific criteria
            server = self.imap_server
            email_address_client = self.email_address
            password = self.password
            imap = imaplib.IMAP4_SSL(server)
            imap.login(email_address_client, password)
            imap.select(email_box)
            key = key
            value = value
            status, messages = imap.search(None, key, value)
            messages = messages[0].split()

            email_found = False

            for mail in messages:
                _, msg = imap.fetch(mail, "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        if date_tuple := email.utils.parsedate_tz(msg["Date"]):
                            email_time = email.utils.mktime_tz(date_tuple)
                            if current_time - email_time <= 15:  # 240 seconds = 4 minutes
                                for part in msg.walk():
                                    if part.get_content_type() == 'text/plain':
                                        text = part.get_payload()
                                        pattern = "\d{3}-\d{3}-\d{3}"
                                        match = re.search(pattern, text)
                                        return match.group() if match else None

                                email_found = True
                                break
                    if email_found:
                        break
            if email_found:
                break
            else:
                time.sleep(delay)
                attempt += 1

            imap.close()
            imap.logout()
