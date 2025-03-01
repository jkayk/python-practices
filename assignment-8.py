from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless") 
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(options=options)

keywords = ["python", "typescript", "javascript"]

def get_total_pages(base_url):
    driver.get(base_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bsj-nav"))
        )
    except:
        print(f"⚠️ No pagination found for {base_url}. Defaulting to 1 page.")
        return 1  # Default to 1 page if pagination is missing

    soup = BeautifulSoup(driver.page_source, "html.parser")

    pagination = soup.find("ul", class_="bsj-nav")

    if pagination:
        page_numbers = [p.text.strip() for p in pagination.find_all(["span", "a"], class_="page-numbers") if p.text.strip().isdigit()]

        if not page_numbers:
            print(f"⚠️ No numeric page numbers found for {base_url}. Defaulting to 1 page.")
            return 1  # Default to 1 page

        total_pages = max(map(int, page_numbers))

        print(f"Found {total_pages} pages for {base_url}.")
        return total_pages
    else:
        print(f"⚠️ No pagination found for {base_url}. Defaulting to 1 page.")
        return 1  # Default to 1 page
    
def get_jobs(base_url, category):
    total_pages = get_total_pages(base_url)  
    all_jobs = []  

    for page in range(1, total_pages + 1): 
        url = f"{base_url}/page/{page}/" if page > 1 else base_url  
        print(f"Scraping: {url}")

        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "bjs-jlid"))
            )
        except:
            print(f"⚠️ Timeout: No job listings found on {url}")
            continue  # Skip to the next page if no jobs are found

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # ✅ Find all job listings (new class: `bjs-jlid`)
        jobs = soup.find_all("li", class_="bjs-jlid")

        if not jobs:
            print(f"⚠️ No jobs found on {url}, skipping...")
            continue  # Skip to the next page if no jobs found

        for job in jobs:
            job_title_elem = job.find("h4", class_="bjs-jlid__h").find("a")
            job_title = job_title_elem.text.strip() if job_title_elem else "N/A"
            
            job_link = job_title_elem["href"] if job_title_elem else "N/A"

            company_elem = job.find("a", class_="bjs-jlid__b")
            company = company_elem.text.strip() if company_elem else "N/A"

            desc_elem = job.find("div", class_="bjs-jlid__description")
            description = desc_elem.text.strip() if desc_elem else "N/A"

            print(f"\nCategory: {category}")
            print(f"Company: {company}")
            print(f"Job Title: {job_title}")
            print(f"Description: {description}")
            print(f"Link: {job_link}")
            print("-" * 80)

get_jobs("https://berlinstartupjobs.com/engineering/", "Engineering")

for keyword in keywords:
    search_url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"
    get_jobs(search_url, keyword)

driver.quit()

print("\n✅ Scraping completed successfully!")