class RegistrationSteps:
    @staticmethod
    def data_for_sent(
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        password: str = None,
    ) -> dict:
        """Registration data to be sent via the REST API

        Args:
            email:      electronic mail;
            first_name: name of the user;
            last_name:  surname of the user;
            password:   password for electronic mail.
        """
        data = {}
        if email:
            data["email"] = email
        if first_name:
            data["firstName"] = first_name
        if last_name:
            data["lastName"] = last_name
        if password:
            data["password"] = password

        return data
