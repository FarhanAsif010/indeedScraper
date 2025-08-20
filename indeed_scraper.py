from base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class IndeedScraper(BaseScraper):
    BASE_URL = "https://pk.indeed.com"

    def build_url(self, job_title, location, start=0):
        return f"{self.BASE_URL}/jobs?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}&start={start}"

    def scrape(self, job_title, location, max_pages=3):
        jobs = []
        
        for page in range(max_pages):
            start = page * 10  # Indeed uses increments of 10
            url = self.build_url(job_title, location, start)
            print(f"Scraping page {page + 1}: {url}")
            
            self.get_page(url)

            # ✅ Wait for job results or bail out if verification page appears
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.ID, "mosaic-jobResults"))
                )
                print("Job results loaded successfully.")
            except:
                print("Verification page detected. Could not scrape this page.")
                self.driver.save_screenshot(f"verification_page_{page+1}.png")
                break  # Stop scraping further pages

            job_cards = self.wait_for_elements("div.job_seen_beacon")
            print(f"Found {len(job_cards)} job cards on page {page + 1}.")

            for card in job_cards:
                title = self.safe_extract(card, "h2.jobTitle > a")
                company = self.safe_extract(card, "span.companyName")
                job_location = self.safe_extract(card, "div.companyLocation")
                date_posted = self.safe_extract(card, "span.date")
                salary = self.safe_extract(card, "div.salary-snippet")
                description = self.safe_extract(card, "div.job-snippet")
                apply_link = self.safe_extract(card, "h2.jobTitle > a", "href")

                if title and apply_link:
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "date_posted": date_posted,
                        "salary": salary,
                        "description": description,
                        "apply_link": f"{self.BASE_URL}{apply_link}" if apply_link.startswith("/") else apply_link,
                        "source": "Indeed"
                    })

            # Optional: small delay to avoid bot detection
            time.sleep(3)

        self.close()
        return jobs
