from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def extract_weworkremotely(keyword):
    print(f"Scraping We Work Remotely for {keyword} jobs...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"https://weworkremotely.com/remote-jobs/search?term={keyword}")

        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        
        jobs = [
            li for li in soup.find_all("li", class_="new-listing-container")
            if "feature--ad" not in li.get("class", [])
        ]
        jobs_db = []

        for job in jobs:
            title = job.find("h4", class_="new-listing__header__title").text
            region = job.select_one("div.new-listing__categories p:last-of-type").text
            company = job.find("p", class_="new-listing__company-name").text
            url = job.find("div", class_="tooltip--flag-logo").next_sibling.get("href")
            job_data = {
                "title": title,
                "company": company,
                "region": region,
                "link": f"https://weworkremotely.com{url}"
            }
            jobs_db.append(job_data)

        browser.close()

    return jobs_db

"""
def save_to_file(file_name, jobs):
    file = open(f"{file_name}_jobs.csv", "w")
    file.write("Title, Company, Region, URL\n")
    for job in jobs:
        file.write(f"{job['title']}, {job['company']}, {job['region']}, {job['link']}\n")
    file.close()

save_to_file("react", extract_weworkremotely("react"))
"""