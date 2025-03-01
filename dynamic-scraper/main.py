from playwright.sync_api import sync_playwright
import time 
from bs4 import BeautifulSoup
import csv

p = sync_playwright().start()  

browser = p.chromium.launch(headless=False) # by default, headless=True
page = browser.new_page()
page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")

# time.sleep(4)
# 
# page.click("button.Aside_searchButton__rajGo")
# 
# time.sleep(4)
# 
# page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
# 
# time.sleep(4)
# 
# page.keyboard.down("Enter")
# 
# time.sleep(4) 
# 
# page.click("a#search_tab_position")
# 
# time.sleep(4)

for x in range(5):
    page.keyboard.down("End")
    time.sleep(4)

content = page.content() # gets the full HTML of the page

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__REty8")
jobs_db = []

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

file = open("jobs.csv", "w") # w stands for write mode. default is read mode. 
writer = csv.writer(file)
writer.writerow(["Title", "Company", "Reward", "URL"])
for jobs_data in jobs_db:
    writer.writerow(jobs_data.values()) 

file.close()