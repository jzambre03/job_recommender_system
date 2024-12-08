
# Job Finder Application

## Overview
The **Job Finder Application** helps users upload their resumes and find jobs tailored to their skills and preferences. By leveraging advanced similarity scoring and external job search APIs, the app matches users with the most relevant job opportunities.

### Key Features
- **Resume Upload**: Users can upload their resumes in PDF or Word format.
- **Job Search**: Enter job title and location to find relevant opportunities.
- **Filters**: Customize the search with options like days old, number of pages, and job sources (Indeed, LinkedIn, etc.).
- **Similarity Scoring**: Matches jobs to the uploaded resume based on content similarity.
- **Download Results**: Export recommended jobs in **CSV** or **Excel** format.

## Technologies Used
- **Frontend**: [Streamlit](https://streamlit.io/) for a lightweight, interactive UI.
- **Backend**: Python Flask API (assumed running on `http://127.0.0.1:5001`).
- **Libraries**:
  - `requests`, `pandas`: API calls and data handling.
  - `PyPDF2`: Extract text from PDF resumes.
  - `gensim`, `nltk`, `scikit-learn`: Text preprocessing and similarity calculation.
  - `tqdm`: Progress tracking.

## Setup and Instructions

### 1. Prerequisites
- Python 3.8 or above installed.
- Package manager `pip` installed.
- Access to job search API services (e.g., Indeed, LinkedIn).

### 2. Install Required Libraries
Run the following command in your terminal to install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Backend API
The backend API is assumed to be running on `http://127.0.0.1:5001`. Ensure that:
- The API endpoint `/recommend_jobs` is operational.
- The API processes POST requests with the following JSON payload:
  ```json
  {
    "resume": "<resume_text>",
    "job_title": "<job_title>",
    "location": "<job_location>",
    "days_old": <number_of_days>,
    "num_pages": <number_of_pages>,
    "include_indeed": true,
    "include_linkedin": true
  }
  ```

To start your backend API:
```bash
python app.py
```


### 4. Run the Streamlit Frontend
To launch the frontend:
```bash
streamlit run main.py
```


### 5. Usage Instructions
1. Open the app in your browser. The default URL is: `http://localhost:8501`.
2. Upload your resume (PDF or Word format).
3. Enter job details (e.g., title, location) and apply additional filters.
4. Click the **"Find Jobs"** button to fetch recommendations.
5. View the recommended jobs in a table and download the results in **CSV** or **Excel** format.

## Troubleshooting
- **API Connection Issues**:
  - Ensure the backend API is running at `http://127.0.0.1:5001`.
  - Verify the `/recommend_jobs` endpoint is reachable.
- **Dependency Errors**:
  - Run `pip install --upgrade <library>` to ensure libraries are up to date.
- **File Upload Issues**:
  - Check file permissions for uploaded resumes.
  - Verify the file format (only PDF and Word are supported).

## Future Enhancements
- Add support for additional job sources like Monster and Glassdoor.
- Integrate a progress bar for job search.
- Enhance similarity scoring with advanced NLP models like BERT.
