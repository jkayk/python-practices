from playwright.sync_api import sync_playwright
import time 
from bs4 import BeautifulSoup
import csv
from file import save_to_csv

keywords = [
    "flutter",
    "react",
    "django"
]

def extract_wanted_jobs(keyword):
    p = sync_playwright().start()  
    browser = p.chromium.launch(headless=False) # by default, headless=True
    page = browser.new_page()

    page.goto(f"https://www.wanted.co.kr/search?query={keyword}&tab=position")
    for x in range(5):
        page.keyboard.down("End")
        time.sleep(3)
    content = page.content() # gets the full HTML of the page
    scrape_page(content)
    save_to_csv(jobs_db, keywords)
    
    p.stop()

jobs_db = []

def scrape_page(content):
    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find_all("div", class_="JobCard_container__REty8")
    for job in jobs:
        title = job.find("strong", class_="JobCard_title__HBpZf").text
        company = job.find("span", class_="JobCard_companyContent___EEde").text
        reward_span = job.find("span", class_="JobCard_reward__cNlG5")
        reward = reward_span.text if reward_span else "N/A"
        link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
        job_data = {
            "title": title,
            "company": company,
            "reward": reward,
            "link": link
        }
        jobs_db.append(job_data)


keyword = input("What do you want to search for?")

wanted = extract_wanted_jobs(keyword)
jobs = wanted

save_to_csv(keyword, jobs)

 