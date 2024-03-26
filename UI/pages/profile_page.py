from .base_page import BasePage
from .locators import ProfilePageLocators


class ProfilePage(BasePage):
    def go_to_edit_page(self):
        button = self.browser.find_element(*ProfilePageLocators.EDIT_BUTTON)
        button.click()




