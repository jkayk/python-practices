from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def extract_berlinstartupjobs(keyword):
    print(f"Scraping Berlin Startup Jobs for {keyword} jobs...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"http://berlinstartupjobs.com/skill-areas/{keyword}/")

        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        
        jobs = soup.find_all("li", class_="bjs-jlid")
        jobs_db = []

        for job in jobs:
            job_title_elem = job.find("h4", class_="bjs-jlid__h").find("a")
            job_title = job_title_elem.text.strip() if job_title_elem else "N/A"
            job_link = job_title_elem["href"] if job_title_elem else "N/A"

            company_name = job.find("a", class_="bjs-jlid__b").text

            job_description = job.find("div", class_="bjs-jlid__description").text

            job_data = {
                "title": job_title,
                "company": company_name,
                "location": "Berlin, Germany", 
                "link": job_link
            }

            jobs_db.append(job_data)

        browser.close()

    return jobs_db

"""
def save_to_file(file_name, jobs):
    file = open(f"{file_name}_jobs.csv", "w")
    file.write("Title, Company, Description, URL\n")
    for job in jobs:
        file.write(f"{job['title']}, {job['company']}, {job['description']}, {job['link']}\n")
    file.close()

save_to_file("python", extract_berlinstartupjobs("python"))
"""