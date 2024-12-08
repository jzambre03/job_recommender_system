from flask import Flask, request, jsonify
from job_search import scrape_indeed_jobs, scrape_linkedin_jobs
from similarity_score import calculate_similarity_tfidf
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/recommend_jobs', methods=['POST'])
def recommend_jobs():
    """
    Endpoint to recommend jobs based on user inputs.
    """
    try:
        # Get JSON data from the request
        data = request.json
        resume = data.get("resume")
        job_title = data.get("job_title")
        location = data.get("location", "")
        days_old = data.get("days_old", 7)
        num_pages = data.get("num_pages", 1)
        include_indeed = data.get("include_indeed", True)
        include_linkedin = data.get("include_linkedin", True)

        if not resume or not job_title:
            return jsonify({"error": "Resume and job title are required"}), 400

        all_jobs = []

        # Fetch jobs from Indeed
        if include_indeed:
            logging.info("Fetching jobs from Indeed...")
            jobs_from_indeed = scrape_indeed_jobs(job_title, location, num_pages)
            all_jobs.extend(jobs_from_indeed)

        # Fetch jobs from LinkedIn
        if include_linkedin:
            logging.info("Fetching jobs from LinkedIn...")
            jobs_from_linkedin = scrape_linkedin_jobs(job_title, location, num_pages)
            all_jobs.extend(jobs_from_linkedin)

        # Add similarity scores to each job
        for job in all_jobs:
            job_description = job.get("Description", "")
            tfidf_score = calculate_similarity_tfidf(resume, job_description) if job_description else 0.0
            job["Similarity Score"] = round(tfidf_score, 4)

        # Sort jobs by similarity score (highest to lowest)
        sorted_jobs = sorted(all_jobs, key=lambda x: x["Similarity Score"], reverse=True)

        return jsonify(sorted_jobs), 200

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
