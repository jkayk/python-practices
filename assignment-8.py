from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# ✅ Set Chrome options (Prevents Blocking & Runs Headless)
options = Options()
options.add_argument("--headless")  # Runs without opening browser (optional)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# ✅ Initialize Selenium WebDriver
driver = webdriver.Chrome(options=options)

# ✅ List of keywords to scrape
keywords = ["python", "typescript", "javascript"]

# ✅ Function to determine total pages dynamically
def get_total_pages(base_url):
    driver.get(base_url)

    try:
        # ✅ Wait for pagination to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bsj-nav"))
        )
    except:
        print(f"⚠️ No pagination found for {base_url}. Defaulting to 1 page.")
        return 1  # Default to 1 page if pagination is missing

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # ✅ Find the pagination bar
    pagination = soup.find("ul", class_="bsj-nav")

    if pagination:
        # ✅ Extract all page numbers (span and a elements)
        page_numbers = [p.text.strip() for p in pagination.find_all(["span", "a"], class_="page-numbers") if p.text.strip().isdigit()]

        if not page_numbers:
            print(f"⚠️ No numeric page numbers found for {base_url}. Defaulting to 1 page.")
            return 1  # Default to 1 page

        # ✅ Get the highest page number safely
        total_pages = max(map(int, page_numbers))

        print(f"✅ Found {total_pages} pages for {base_url}.")
        return total_pages
    else:
        print(f"⚠️ No pagination found for {base_url}. Defaulting to 1 page.")
        return 1  # Default to 1 page
    
# ✅ Function to scrape job listings
def get_jobs(base_url, category):
    total_pages = get_total_pages(base_url)  # Get the total number of pages dynamically
    all_jobs = []  # Store all job listings from multiple pages

    for page in range(1, total_pages + 1):  # Loop through pages (1 to total_pages)
        url = f"{base_url}/page/{page}/" if page > 1 else base_url  # Handle first page separately
        print(f"🔍 Scraping: {url}")

        driver.get(url)

        try:
            # ✅ Wait until at least one job listing appears
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
            # ✅ Get Job Title
            job_title_elem = job.find("h4", class_="bjs-jlid__h").find("a")
            job_title = job_title_elem.text.strip() if job_title_elem else "N/A"
            
            # ✅ Get Job Link
            job_link = job_title_elem["href"] if job_title_elem else "N/A"

            # ✅ Get Company Name
            company_elem = job.find("a", class_="bjs-jlid__b")
            company = company_elem.text.strip() if company_elem else "N/A"

            # ✅ Get Job Description
            desc_elem = job.find("div", class_="bjs-jlid__description")
            description = desc_elem.text.strip() if desc_elem else "N/A"

            # ✅ Print job details to console
            print(f"\n🔹 Category: {category}")
            print(f"🏢 Company: {company}")
            print(f"💼 Job Title: {job_title}")
            print(f"📝 Description: {description}")
            print(f"🔗 Link: {job_link}")
            print("-" * 80)

# ✅ Scrape jobs from the general "Engineering" page first
get_jobs("https://berlinstartupjobs.com/engineering/", "Engineering")

# ✅ Loop through each keyword and scrape jobs
for keyword in keywords:
    search_url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"
    get_jobs(search_url, keyword)

# ✅ Close the Selenium driver
driver.quit()

print("\n✅ Scraping completed successfully!")