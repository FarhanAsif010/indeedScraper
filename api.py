from fastapi import FastAPI
from pydantic import BaseModel
from indeed_scraper import IndeedScraper

app = FastAPI()

class SearchCriteria(BaseModel):
    job_title: str
    location: str

@app.post("/scrape_jobs")
def scrape_jobs(criteria: SearchCriteria):
    scraper = IndeedScraper(headless=False)  # Set True if you want background mode
    jobs = scraper.scrape(criteria.job_title, criteria.location)
    print(jobs)  # Debug output
    return {"jobs": jobs}

@app.get("/")
def read_root():
    return {"message": "Scraper is running"}
