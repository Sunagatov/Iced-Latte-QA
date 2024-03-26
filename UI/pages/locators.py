from selenium.webdriver.common.by import By


class BasePageLocators:
    LOGIN_LINK = (By.CSS_SELECTOR, '[href="/auth/login"]')
    PROFILE_LINK = (By.CSS_SELECTOR, '[href="/profile"]')


class LoginPageLocators:
    REGISTER_BUTTON = (By.CSS_SELECTOR, '[href="/auth/registration"]')
    EMAIL_FIELD = (By.ID, 'email')
    PASSWORD_FIELD = (By.ID, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')


class RegistrationPageLocators:
    FIRST_NAME_FIELD = (By.ID, 'firstName')
    LAST_NAME_FIELD = (By.ID, 'lastName')
    EMAIL_FIELD = (By.ID, 'email')
    PASSWORD_FIELD = (By.ID, 'password')
    REGISTER_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')


class ProfilePageLocators:
    EDIT_BUTTON = (By.LINK_TEXT, 'Edit')


class EditProfilePageLocators:
    FIRST_NAME_FIELD = (By.ID, 'firstName')

