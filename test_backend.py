import requests

# Backend URL
url = "http://127.0.0.1:5001/recommend_jobs"

# Payload to send
payload = {
    "resume": "Proficient in Python and data analysis.",
    "job_title": "Data Scientist",
    "location": "San Francisco",
    "days_old": 7,
    "num_pages": 1,
    "include_indeed": True,
    "include_linkedin": True
}

# Send the POST request
response = requests.post(url, json=payload)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())