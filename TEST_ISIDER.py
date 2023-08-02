import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver


class HomePage(BasePage):
    URL = "https://useinsider.com/"
    TITLE = "Insider"

    def open(self):
        self.driver.get(self.URL)

    def is_page_opened(self):
        return self.TITLE in self.driver.title

    def is_element_present(self, by, value):
        try:
            self.driver.find_element(by, value)
            return True
        except:
            return False

    def click_company_menu(self):
        company_menu = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Company"))
        )
        company_menu.click()

    def click_careers(self):
        careers_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Careers")))
        careers_link.click()

    def is_career_page_opened(self):
        return "careers" in self.driver.current_url.lower()

    def accept_all_cookies(self):
        try:
            accept_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "wt-cli-accept-all-btn")))
            accept_button.click()
        except:
            pass


class CareersPage(BasePage):
    URL = "https://useinsider.com/careers/"
    TITLE = "Insider Careers"

    def open(self):
        self.driver.get(self.URL)

    def is_page_opened(self):
        return self.TITLE in self.driver.title

    def click_see_all_teams(self):
        try:
            see_all_teams_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "career-find-our-calling")))
            see_all_teams_button.click()
        except Exception as e:
            raise AssertionError(f"Failed to click 'See all teams' button. Error: {e}")

    def accept_all_cookies(self):
        pass


@pytest.fixture(params=["chrome", "firefox"], scope="class")
def browser(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError("Invalid browser specified.")

    yield driver
    driver.quit()


@pytest.mark.usefixtures("browser")
class TestInsiderHomePage:
    def test_insider_home_page_opened(self, browser):
        home_page = HomePage(browser)
        home_page.open()
        home_page.accept_all_cookies()
        assert home_page.is_page_opened(), "Insider home page is not opened."

    def test_insider_home_page_title(self, browser):
        home_page = HomePage(browser)
        home_page.open()
        home_page.accept_all_cookies()

        assert home_page.is_page_opened(), "Insider home page is not opened."
        assert home_page.TITLE in browser.title, f"Expected title: {home_page.TITLE}, Actual title: {browser.title}"

    def test_career_page_opened(self, browser):
        careers_page = CareersPage(browser)
        careers_page.open()
        careers_page.accept_all_cookies()

    def test_see_all_teams_button(self, browser):
        careers_page = CareersPage(browser)
        careers_page.open()
        careers_page.accept_all_cookies()
        careers_page.click_see_all_teams()


class TestQualityAssuranceButton:
    @pytest.mark.usefixtures("browser")
    def test_quality_assurance_button(self, browser):
        url = "https://useinsider.com/careers/"
        browser.get(url)

        # Wait for the "Accept All" button to be clickable and accept all cookies
        wait = WebDriverWait(browser, 15)
        accept_all_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "wt-cli-accept-all-btn")))
        accept_all_button.click()

        # Wait for the "See all teams" button to be clickable and click on it
        see_all_teams_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "See all teams")))
        browser.execute_script("arguments[0].click();", see_all_teams_button)

        # Find the "Quality Assurance" button and click on it
        quality_assurance_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[text()='Quality Assurance']")))
        browser.execute_script("arguments[0].click();", quality_assurance_button)

        # Wait for the "See all QA jobs" button to be clickable and click on it
        see_all_qa_jobs_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='See all QA jobs']")))
        see_all_qa_jobs_button.click()

        # Check that the page has the expected title and URL
        expected_title = "Insider Open Positions | Insider"
        assert expected_title in browser.title
        assert browser.current_url == "https://useinsider.com/careers/open-positions/?department=qualityassurance"


if __name__ == "__main__":
    # Create a 'screenshots' directory if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # Run the test case
    pytest.main(["-v", "test_insider_home_page.py"])
