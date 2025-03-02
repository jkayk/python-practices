from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup

def scrape_jobs(page):
    content = page.content()
    soup = BeautifulSoup(content, "html.parser")

    jobs_db = []

    jobs = [
        tr for tr in soup.find_all("tr", class_="table_row")
        if "border-paid-table" not in tr.get("class", [])
    ]

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
    
    return jobs_db

def extract_web3(keyword):
    print(f"Scraping We Work Remotely for {keyword} jobs...")
    
    p = sync_playwright().start()  
    browser = p.chromium.launch(headless=False) 
    page = browser.new_page(
        extra_http_headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
    )
    stealth_sync(page)
    page.goto(f"https://web3.career/{keyword}-jobs?page=1")

    all_jobs_db = []

    while True:
        # Perform scraping on the current page
        jobs = scrape_jobs(page)
        all_jobs_db.extend(jobs)

        # Check if the "Next" button is disabled
        next_button_li = page.locator("ul.pagination li.next")  # Locate the <li> of "Next"
        if next_button_li.get_attribute("class") == "page-item next disabled":
            break  # Stop if "Next" is disabled

        # Click "Next" button and wait for the page to load
        next_button = next_button_li.locator("a.page-link")
        next_button.click()
        page.wait_for_load_state("domcontentloaded")

    browser.close()
    return all_jobs_db

def save_to_file(file_name, jobs):
    file = open(f"{file_name}_jobs.csv", "w")
    file.write("Title, Company, Location, URL\n")
    for job in jobs:
        file.write(f"{job['title']}, {job['company']}, {job['location']}, {job['link']}\n")
    file.close()

save_to_file("python", extract_web3("python"))