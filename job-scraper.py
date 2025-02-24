import requests
from bs4 import BeautifulSoup

url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs#job-listings"

res = requests.get(url)

soup = BeautifulSoup(res.content, "html.parser")

jobs = soup.find("section", class_="jobs").find_all("li")
