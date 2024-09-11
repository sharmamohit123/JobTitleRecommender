# import boto3
import pandas as pd
import numpy as np
import json
# import yaml
import time

# import datetime
import streamlit as st


# Streamlit app
def main():
    st.sidebar.title("Jobseeker")

    df = pd.read_csv('js_data_sample_with_gpt_resp.parquet')
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

    # Display relevant job titles at the bottom right
    if st.button("Generate Relevant Job Titles"):
        jobseeker_info['gpt_4o_resp']

if __name__ == "__main__":
    main()
