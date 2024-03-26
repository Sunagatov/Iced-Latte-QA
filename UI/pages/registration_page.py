from .base_page import BasePage
from .locators import RegistrationPageLocators


class RegistrationPage(BasePage):
    def register_new_user(self, first_name, last_name, email, password):
        first_name_field = self.browser.find_element(*RegistrationPageLocators.REGISTER_FIRST_NAME_FIELD)
        first_name_field.send_keys(first_name)
        last_name_field = self.browser.find_element(*RegistrationPageLocators.REGISTER_LAST_NAME_FIELD)
        last_name_field.send_keys(last_name)
        email_field = self.browser.find_element(*RegistrationPageLocators.REGISTER_EMAIL_FIELD)
        email_field.send_keys(email)
        password_field = self.browser.find_element(*RegistrationPageLocators.REGISTER_PASSWORD_FIELD)
        password_field.send_keys(password)
        register_button = self.browser.find_element(*RegistrationPageLocators.REGISTER_BUTTON)
        register_button.click()
