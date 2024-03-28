from .base_page import BasePage
from .locators import EditProfilePageLocators


class EditProfilePage(BasePage):
    def change_first_name(self, new_first_name):
        first_name_field = self.browser.find_element(*EditProfilePageLocators.FIRST_NAME_FIELD)
        first_name_field.clear()
        first_name_field.send_keys(new_first_name)

    def save_change(self):
        save_change_button = self.browser.find_element(*EditProfilePageLocators.SAVE_CHANGE_BUTTON)
        save_change_button.click()
