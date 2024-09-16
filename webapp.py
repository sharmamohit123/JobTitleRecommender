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
    st.set_page_config(
        page_title="JobRecommender",
        page_icon=":apply:",
        # layout="wide",
        initial_sidebar_state="auto",
    )
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

    df = pd.read_csv('js_gpt_careerist_next_as_titles_sampled_v2.parquet')
    # df = read_feature_json(S3_PATH)
    # df['resume_data_combined'] = df.apply(lambda x: make_data(x), axis=1)

    # Dropdown to select jobseeker-id
    jobseeker_id = st.sidebar.selectbox("Select Jobseeker ID", df['accountId'])

    # Fetching jobseeker info based on selected ID
    jobseeker_info = df[df['accountId'] == jobseeker_id].iloc[0]

    # Display jobseeker information on the right side
    st.title("Jobseeker Information")
    st.subheader("Resume Summary")
    st.write(jobseeker_info['js_exp_summary'])

    # st.subheader("Experience")
    # st.write(jobseeker_info['experience'])

    st.subheader("Past Applies")
    st.write(jobseeker_info['jsAppliedJobTitles'])
    st.subheader("Past Clicks")
    st.write(jobseeker_info['jsClickedJobTitles'])
    st.subheader("Past Searches")
    st.write(jobseeker_info['jsSearchQueries'])
    # st.write(jobseeker_info['resume_data_combined'])

    # Right sidebar for applied jobs in the next few days
    # st.sidebar.title("Upcoming Applied Jobs")
    st.sidebar.subheader("Jobseeker Next ApplyStarted job titles")
    applied_jobs = jobseeker_info['next_as_job_titles']
    for job in ast.literal_eval(applied_jobs):
        st.sidebar.write(f"- {job}")

    st.sidebar.subheader("Careerist MP job titles")
    careerist_jobs = jobseeker_info['careerist_job_titles']
    for job in ast.literal_eval(careerist_jobs):
        st.sidebar.write(f"- {job}")

    # Display relevant job titles at the bottom right
    if st.button("Generate Relevant Job Titles"):

        st.title("GPT Suggested Job Titles")
        
        st.markdown("""
        :blue-background[**Disclaimer**: The quality of the recommended job titles depends on the richness of the resume data 
        and past job activity. The more detailed and up-to-date the information, 
        the better the recommendations will be.]
        """)

        # print(jobseeker_info['gpt_4o_resp'])
        # jobseeker_info['gpt_4o_resp']['job_recommendations']
        response_json = json.loads("\n".join(jobseeker_info['gpt_4o_resp'].splitlines()[1:-1]))
        llm_job_titles = [m['title'] for m in response_json['job_recommendations']]
        llm_job_justifications = [m['justification'] for m in response_json['job_recommendations']]
        for idx, job in enumerate(llm_job_titles):
            # print(job)
            st.subheader(f"- {job}")
            st.write(f"Justification: {llm_job_justifications[idx]}")

if __name__ == "__main__":
    main()
