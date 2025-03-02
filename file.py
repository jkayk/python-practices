import csv

def save_to_csv(file_name, jobs):
    file = open("f{file_name}_jobs.csv", "w")
    file.write("Title, Company, Reward, URL\n")
    for job in jobs:
        file.write(f"{job['title']}, {job['company']}, {job['reward']}, {job['link']}\n")
    file.close()