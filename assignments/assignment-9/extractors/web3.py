from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def extract_web3(keyword):
    print(f"Scraping We Work Remotely for {keyword} jobs...")
    
    p = sync_playwright().start()  

    browser = p.chromium.launch() 
    page = browser.new_page()
    page.goto(f"https://web3.career/{keyword}-jobs")

    content = page.content()
    soup = BeautifulSoup(content, "html.parser")
    
    jobs = soup.find_all("tr", class_="table_row")
    jobs = [
        tr for tr in soup.find_all("tr", class_="table_row")
        if "border-paid-table" not in tr.get("class", [])
    ]

    jobs_db = []

    for job in jobs:
        job_title_elem = job.find("div", class_="job-title-mobile").find("a").find("h2")
        job_title = job_title_elem.text.strip() if job_title_elem else "N/A"        

        company = job.find("h3").text
        
        location_tds = job.find_all("td", class_="job-location-mobile")
        if len(location_tds) > 1:
            location_td = location_tds[1]   
        location_parts = [a.text.strip() for a in location_td.find_all("a")]
        location = ", ".join(location_parts)
        
        url = job.find("div", class_="job-title-mobile").find("a")["href"]
        
        job_data = {
            "title": job_title,
            "company": company,
            "location": location,
            "link": f"https://web3.career{url}"
        }
        
        jobs_db.append(job_data)

    print("Finished scraping Web3.")
    return jobs_db

def save_to_file(file_name, jobs):
    file = open(f"{file_name}_jobs.csv", "w")
    file.write("Title, Company, Location, URL\n")
    for job in jobs:
        file.write(f"{job['title']}, {job['company']}, {job['location']}, {job['link']}\n")
    file.close()

save_to_file("python", extract_web3("python"))