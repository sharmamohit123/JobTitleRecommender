# import boto3
import pandas as pd
import numpy as np
import json
# import yaml
import time
import ast
# import datetime
import streamlit as st


# Streamlit app
def main():
    # Custom CSS to adjust sidebar width
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            width: 400px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.title("Jobseeker")

    df = pd.read_csv('js_gpt_careerist_next_as_titles_sampled.parquet')
    # df = read_feature_json(S3_PATH)
    # df['resume_data_combined'] = df.apply(lambda x: make_data(x), axis=1)

    # Dropdown to select jobseeker-id
    jobseeker_id = st.sidebar.selectbox("Select Jobseeker ID", df['accountId'])

    # Fetching jobseeker info based on selected ID
    jobseeker_info = df[df['accountId'] == jobseeker_id].iloc[0]

    # Display jobseeker information on the right side
    st.title("Jobseeker Information")
    # st.subheader("Resume Summary")
    # st.write(jobseeker_info['resume_summary'])

    # st.subheader("Experience")
    # st.write(jobseeker_info['experience'])

    # st.subheader("Past Activity")
    # st.write(jobseeker_info['past_activity'])
    st.write(jobseeker_info['resume_data_combined'])

    # Right sidebar for applied jobs in the next few days
    # st.sidebar.title("Upcoming Applied Jobs")
    st.sidebar.subheader("Jobseeker next ApplyStarted job titles")
    applied_jobs = jobseeker_info['next_as_job_titles']
    for job in ast.literal_eval(applied_jobs):
        st.sidebar.write(f"- {job}")

    st.sidebar.subheader("Careerist MP job titles")
    careerist_jobs = jobseeker_info['careerist_job_titles']
    for job in ast.literal_eval(careerist_jobs):
        st.sidebar.write(f"- {job}")

    # Display relevant job titles at the bottom right
    if st.button("Generate Relevant Job Titles"):
        jobseeker_info['gpt_4o_resp']

if __name__ == "__main__":
    main()
