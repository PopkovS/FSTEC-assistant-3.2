import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import modules.pg_data_base as pgdb


def pytest_addoption(parser):
    parser.addoption('--browser_name',
                     action='store',
                     default="chrome",
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language',
                     action='store',
                     default='en',
                     help="Choose language")


@pytest.fixture(scope="session")
def browser(request):
    user_language = request.config.getoption("language")
    browser_name = request.config.getoption("browser_name")
    browser = None
    if browser_name == "chrome":
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        options.add_argument("--window-size=1600,900")
        # options.add_argument("--headless")
        print("\nstart chrome browser for test..")
        # browser = webdriver.Chrome(options=options)   #На случай если не удасться запустить драйвер менеджер
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # browser.maximize_window()
    elif browser_name == "firefox":
        fp = webdriver.FirefoxProfile()
        fp.set_preference("intl.accept_languages", user_language)
        print("\nstart firefox browser for test..")
        browser = webdriver.Firefox(firefox_profile=fp)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser

    print("\nquit browser..")
    browser.quit()