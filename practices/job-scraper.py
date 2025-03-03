import requests
from bs4 import BeautifulSoup

all_jobs = []

def scrape_page(url):

    print(f"Scraping {url}...")
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    jobs = [
        li for li in soup.find("section", class_="jobs").find_all("li", class_="new-listing-container")
        if "feature--ad" not in li.get("class", [])
    ][0:-1]

    for job in jobs:
        title = job.find("h4", class_="new-listing__header__title").text
        region = job.select_one("div.new-listing__categories p:last-of-type").text
        company = job.find("p", class_="new-listing__company-name").text
        url = job.find("div", class_="tooltip--flag-logo").next_sibling.get("href")
        job_data = {
            "title": title,
            "region": region,
            "company": company,
            "url": f"https://weworkremotely.com{url}"
        }
        all_jobs.append(job_data)

def get_pages(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    return len(soup.find("div", class_="pagination").find_all("span", class_="page")) # len() gives you the length of a list and find_all() returns a list of elements

total_pages = get_pages("https://weworkremotely.com/remote-full-time-jobs?page=1") # 4

# for x in range(y) is a loop that will run y times

for x in range(total_pages): # range(4)
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}" # because the page starts at 1 and not 0
    scrape_page(url)

print(len(all_jobs))