# import streamlit as st
# import requests
# import pandas as pd
# from PyPDF2 import PdfReader
# from io import BytesIO  # For creating in-memory Excel files

# # Streamlit Page Configuration
# st.set_page_config(page_title="Job Finder", layout="wide")

# # Title
# st.title("Job Recommender System")
# st.subheader("Upload your resume and find the best jobs for you!")

# # Resume Upload Function
# def extract_text_from_pdf(file):
#     reader = PdfReader(file)
#     text = " ".join(page.extract_text() for page in reader.pages)
#     return text

# # Resume Upload
# uploaded_file = st.file_uploader("Upload your resume (PDF or Word)", type=["pdf", "docx"])
# if uploaded_file:
#     if uploaded_file.type == "application/pdf":
#         resume_text = extract_text_from_pdf(uploaded_file)
#     else:
#         resume_text = uploaded_file.read().decode("utf-8", errors="ignore")
#     st.success("Resume uploaded successfully!")
# else:
#     resume_text = None

# # Job Search Inputs
# job_title = st.text_input("Enter job title:")
# job_location = st.text_input("Enter job location:")

# # Additional Filters
# days_old = st.number_input("Filter jobs posted in the last X days:", min_value=1, max_value=30, value=7)
# num_pages = st.number_input("Number of pages to fetch:", min_value=1, max_value=10, value=1)

# # Include Source Options
# st.write("Include Results From:")
# include_indeed = st.checkbox("Indeed", value=True)
# include_linkedin = st.checkbox("LinkedIn", value=True)

# if st.button("Find Jobs"):
#     if not resume_text or not job_title:
#         st.error("Please upload a resume and provide a job title!")
#     else:
#         # Call the backend API
#         try:
#             response = requests.post("http://127.0.0.1:5001/recommend_jobs", json={
#                 "resume": resume_text,
#                 "job_title": job_title,
#                 "location": job_location,
#                 "days_old": days_old,
#                 "num_pages": num_pages,
#                 "include_indeed": include_indeed,
#                 "include_linkedin": include_linkedin
#             })

#             if response.status_code == 200:
#                 jobs = response.json()
#                 if jobs:
#                     # Convert JSON response to DataFrame
#                     jobs_df = pd.DataFrame(jobs)

#                     # Select and display relevant columns
#                     if not jobs_df.empty:
#                         st.write("Recommended Jobs:")
#                         st.dataframe(jobs_df[["Title", "Company", "Location", "Similarity Score", "Link", "Description"]])

#                         # Save the DataFrame as CSV
#                         csv_data = jobs_df.to_csv(index=False)

#                         # Save the DataFrame as Excel using BytesIO
#                         excel_buffer = BytesIO()
#                         jobs_df.to_excel(excel_buffer, index=False, engine='openpyxl')
#                         excel_data = excel_buffer.getvalue()

#                         # Download Buttons
#                         st.download_button(
#                             label="Download as CSV",
#                             data=csv_data,
#                             file_name="recommended_jobs.csv",
#                             mime="text/csv",
#                         )
#                         st.download_button(
#                             label="Download as Excel",
#                             data=excel_data,
#                             file_name="recommended_jobs.xlsx",
#                             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                         )
#                     else:
#                         st.write("No jobs found matching your criteria.")
#                 else:
#                     st.write("No jobs found matching your criteria.")
#             else:
#                 st.error(f"Failed to fetch jobs: {response.status_code}")

#         except Exception as e:
#             st.error(f"Error occurred: {str(e)}") 