from pages.base_page import BasePage
from pages.login_page import LoginPage
from configs import link, first_name, last_name, email, password


from time import sleep
from allure import description, step, title, feature, severity, story


@title("Test Change First Name")
@story("Personal Account")
# @allure.description("")
# @allure.tag("")
@severity(allure.severity_level.MAJOR)
def test_user_can_change_first_name(browser):
    with step('Open main page'):
        page = BasePage(browser, link)
        page.open()
    with step('Go to login page'):
        page.go_to_login_page()
    with step('Login existing user'):
        login_page = LoginPage(browser, browser.current_url)
        login_page.login_existing_user()




    sleep(5)
