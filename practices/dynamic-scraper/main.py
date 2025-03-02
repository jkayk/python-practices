from playwright.sync_api import sync_playwright
import time 
from bs4 import BeautifulSoup
import csv

jobs_db = []

def extract_wanted(keyword):

    p = sync_playwright().start()  

    browser = p.chromium.launch(headless=False) # by default, headless=True
    page = browser.new_page()
    page.goto(f"https://www.wanted.co.kr/search?query={keyword}&tab=position")

    for x in range(5):
        page.keyboard.down("End")
        time.sleep(4)

    content = page.content() # gets the full HTML of the page
    
    p.stop()
    scrape_page(content)
    save_to_csv(jobs_db, keyword)

def scrape_page(content):

    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find_all("div", class_="JobCard_container__REty8")

    for job in jobs:
        title = job.find("strong", class_="JobCard_title__HBpZf").text
        company = job.find("span", class_="JobCard_companyContent___EEde").text
        reward = job.find("span", class_="JobCard_reward__cNlG5").text
        url = f"https://www.wanted.co.kr/{job.find('a')['href']}"
        job_data = {
            "title": title,
            "company": company,
            "reward": reward,
            "url": url
        }
        jobs_db.append(job_data)

def save_to_csv(jobs_db, keyword):
    file = open(f"{keyword}.csv", "w") # w stands for write mode. default is read mode. 
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Reward", "URL"])
    for jobs_data in jobs_db:
        writer.writerow(jobs_data.values()) 
    file.close()


extract_wanted("python")