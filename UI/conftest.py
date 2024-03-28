import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

    
def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='en',
                     help="Choose language: es, ru or en")


@pytest.fixture(scope="function")
def browser(request):            
    options = webdriver.ChromeOptions()
    # turn off Chrome service message
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # get language from cmd
    user_language = request.config.getoption("language")
    # turn on Chrome language support
    options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
    # turn on FF language support
    options_ff = Options()
    options_ff.set_preference("intl.accept_languages", user_language)
    # get browser from cmd
    browser_name = request.config.getoption("browser_name")
    browser = None
    if browser_name == "chrome":
        print("\nstart chrome browser for test..")        
        browser = webdriver.Chrome(options=options)        
    elif browser_name == "firefox":
        print("\nstart firefox browser for test..")
        browser = webdriver.Firefox(options=options_ff)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser
    print("\nquit browser..")
    browser.quit()
    