from .base_page import BasePage
from .locators import LoginPageLocators


class LoginPage(BasePage):
    def go_to_registration_page(self):
        link = self.browser.find_element(*LoginPageLocators.REGISTER_BUTTON)
        link.click()

    def login_existing_user(self, email, password):
        email_field = self.browser.find_element(*LoginPageLocators.EMAIL_FIELD)
        password_field = self.browser.find_element(*LoginPageLocators.PASSWORD_FIELD)
        login_button = self.browser.find_element(*LoginPageLocators.LOGIN_BUTTON)
        email_field.send_keys(email)
        password_field.send_keys(password)
        login_button.click()
