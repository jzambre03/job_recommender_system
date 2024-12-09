from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import randint
import math 
import logging
logging.disable(logging.CRITICAL)
import json
import math
import http.client
import json
import logging
from selenium.webdriver.common.keys import Keys
import pandas as pd
import PyPDF2
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import re
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

def get_webdriver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_indeed_jobs(job_title, location, page = 1):
    jobs_per_page = 10  # Number of jobs per page
    base_url = "https://www.indeed.com/jobs"
    url_template = f"?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}&sort=date"

    job_list = []  # List to store all job details
    seen_jobs = set()  # To track unique jobs based on (Title, Company, Location)
    num_jobs = page * 15
    
    for i in range(page):
        start = i * jobs_per_page
        url = base_url + url_template + f"&start={start}"
        driver = get_webdriver()
        driver.get(url)
        time.sleep(2)

        while True:
            try:
                # Wait for the job listings to load
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon")))
            except Exception as e:
                break

            # Parse the current page
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract job postings
            jobs = soup.find_all("div", class_="job_seen_beacon")

            if not jobs:
                break  # Stop if no jobs are found

            for job in jobs:
                try:
                    title_element = job.find("span", id=lambda x: x and x.startswith("jobTitle"))
                    title = title_element.text.strip() if title_element else "N/A"

                    company_element = job.find("span", attrs={"data-testid": "company-name"})
                    company = company_element.text.strip() if company_element else "N/A"

                    location_element = job.find("div", attrs={"data-testid": "text-location"})
                    job_location = location_element.text.strip() if location_element else "N/A"
                    
                    # Create a unique identifier for the job
                    job_id = (title, company, job_location)
                    
                    if job_id in seen_jobs:
                        continue  # Skip this job if it's a duplicate

                    # Add to the set of seen jobs
                    seen_jobs.add(job_id)

                    # Extract job link
                    link_element = job.find("a", href=True)
                    job_link = "https://www.indeed.com" + link_element["href"] if link_element else "N/A"

                    # Visit the job link to fetch the description
                    description = "N/A"
                    if job_link != "N/A":
                        driver = get_webdriver()
                        driver.get(job_link)
                        time.sleep(2)  # Allow the job description to load
                        job_page_html = driver.page_source
                        job_soup = BeautifulSoup(job_page_html, "html.parser")
                        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "jobDescriptionText")))
                        description_element = driver.find_element(By.ID, "jobDescriptionText")
                        description = description_element.text.strip() if description_element else "N/A"

                    # Append job details to the list
                    job_list.append({
                        "Title": title,
                        "Company": company,
                        "Location": job_location,
                        "Link": job_link,
                        "Description": description,
                    })

                except Exception as e:
                    print(f"Error extracting job: {e}")
                    
                # Stop if we've collected the required number of jobs
                if len(job_list) >= num_jobs:
                    break


    driver.quit()
    return job_list



def scrape_linkedin_jobs(search_term, location, page = 1):
    # Access variables
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    JOB_SEARCH_URL = os.getenv("JOB_SEARCH_URL")
    JOB_SEARCH_X_RAPIDAPI_HOST = os.getenv("JOB_SEARCH_X_RAPIDAPI_HOST")
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    try:
        # Establish connection to RapidAPI
        conn = http.client.HTTPSConnection(JOB_SEARCH_X_RAPIDAPI_HOST)

        # API request payload
        payload = json.dumps({
            "search_terms": search_term,
            "location": location,
            "page": page
        })

        # Request headers
        headers = {
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": JOB_SEARCH_X_RAPIDAPI_HOST,
            "Content-Type": "application/json"
        }

        # Send POST request
        conn.request("POST", "/", payload, headers)
        res = conn.getresponse()
        data = res.read()

        # Parse JSON response
        json_response = json.loads(data.decode("utf-8"))
        logging.info(f"API Response: {json_response}")

    except Exception as e:
        logging.error(f"Error fetching jobs: {e}")

#    driver = webdriver.Chrome()
    driver = get_webdriver()
    driver.get("https://www.linkedin.com/login")
    
    # Find and fill the username field
    driver.find_element(By.ID, "username").send_keys(email)
    
    # Find and fill the password field
    driver.find_element(By.ID, "password").send_keys(password)
    
    # Click the login button
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    # Wait for the next page to load
    time.sleep(5)
    
    jobs_list = []
    if isinstance(json_response, list):  # Ensure the response is a list
        for job in json_response:  # Iterate directly over the list
            job_url = job.get("linkedin_job_url_cleaned")
            job_description = ""
            # Fetch job description
            #job_description = fetch_job_description(driver, job_url)
            
            driver.get(job_url)
            time.sleep(5)  # Allow time for the page to load fully
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Look for the job description
            description_div = soup.find('div', {'class': 'jobs-description__content'})
            if not description_div:
                return "Job description not found or unable to parse. Check the HTML structure."

            # Extract and return the text
            job_description = description_div.get_text(strip=True)

            # Create a dictionary for each job
            job_details = {
                "Title": job.get("job_title"),
                "Company": job.get("company_name"),
                "Location": job.get("job_location"),
                "Link": job.get("linkedin_job_url_cleaned"),
                "Description": job_description
            }
            # Append the dictionary to the list
            jobs_list.append(job_details)
        driver.quit()
    else:
        # Print error if results are not a list
        print("Error:", json_response.get("error", "Unknown error occurred"))


    return jobs_list