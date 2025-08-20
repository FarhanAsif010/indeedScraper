import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseScraper:
    def __init__(self, headless=True):
        options = uc.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        self.driver = uc.Chrome(options=options)

    def get_page(self, url):
        self.driver.get(url)
        self.random_delay()
        if "captcha" in self.driver.page_source.lower() or "verify you are human" in self.driver.page_source.lower():
            print("⚠ CAPTCHA detected! Please solve it manually.")
            time.sleep(20)  # Give time to solve manually

    def wait_for_element(self, css_selector, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
        except:
            return None

    def wait_for_elements(self, css_selector, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
            )
        except:
            return []

    def safe_extract(self, element, selector, attr=None):
        try:
            sub_elem = element.find_element(By.CSS_SELECTOR, selector)
            if attr:
                return sub_elem.get_attribute(attr)
            return sub_elem.text.strip()
        except:
            return None

    def random_delay(self):
        time.sleep(random.uniform(2, 5))

    def close(self):
        self.driver.quit()
