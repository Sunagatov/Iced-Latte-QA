from imap_tools import MailBox, A
import re
from typing import Union
import time


class Email:
    def __init__(self, imap_server: str, email_address: str, mail_password: str):
        self.imap_server = imap_server
        self.email_address = email_address
        self.password = mail_password

    def connect_mailbox(self, email_box: str):
        """Method to establish a connection to the mailbox.

        Args:
            email_box: The email folder to connect to.

        Returns:
            MailBox: The connected mailbox object.
        """
        return MailBox(self.imap_server).login(self.email_address, self.password, initial_folder=email_box)

    def extract_confirmation_code_from_email(self, email_box: str, key: str, value: str) -> Union[str, None]:
        """Method for extraction confirmation code for registration from user's email.

        Args:
            email_box: email's folder, where search is performed
            key: criterion to search message through email (e.g., "FROM")
            value: value for the search criterion (e.g., "email.email@gmail.com")
        """
        attempt = 0
        delay = 10
        max_attempts = 4
        while attempt < max_attempts:
            current_time = time.time()

            with self.connect_mailbox(email_box) as mailbox:
                messages = mailbox.fetch(criteria=A(**{key.lower(): value}), mark_seen=False, bulk=True)
                for msg in messages:
                    email_time = msg.date.timestamp()
                    if current_time - email_time <= 13.5:
                        text = msg.text or ""
                        pattern = "\d{3}-\d{3}-\d{3}"
                        match = re.search(pattern, text)
                        if match:
                            return match.group()

            time.sleep(delay)
            attempt += 1

        return None
