def save_to_file(file_name, jobs):
    file = open(f"{file_name}_jobs.csv", "w")
    file.write("Title, Company, Description, URL\n")
    for job in jobs:
        file.write(f"{job['title']}, {job['company']}, {job['description']}, {job['link']}\n")
    file.close()