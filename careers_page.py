import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TEST_FRAMEWORK import BasePage


class CareersPage(BasePage):
    CAREERS_URL = "https://useinsider.com/careers"
    CAREERS_TITLE = "Careers at Insider"

    def open_careers_page(self):
        self.driver.get(self.CAREERS_URL)

    def is_careers_page_opened(self):
        return self.CAREERS_TITLE in self.driver.title
