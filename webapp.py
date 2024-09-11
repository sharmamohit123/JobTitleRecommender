# import boto3
import pandas as pd
import numpy as np
import json
# import yaml
import time

# import datetime
import openai
import streamlit as st

# S3_PATH = 'features/HP/2024-07-10_2024-07-11'
# S3_BUCKET = 'mrp-rm-explore-llm-match-labeler-prod'

# @st.cache_data
# def read_feature_json(prefix, show_file_keys=False):
#     response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
#     dfs = []
#     for item in response.get("Contents"):
#         key = item.get("Key")
#         if show_file_keys:
#             print(key)
#         object_response = s3_client.get_object(Bucket=S3_BUCKET, Key=key)
#         file_content = object_response.get("Body").read()
#         df = pd.read_json(file_content.decode(), lines=True)
#         dfs.append(df)
#     return pd.concat(dfs, ignore_index=True).replace({np.nan: None})

# def get_skills_experience(q):
#     if (q.get('experience', 0) > 0):
#         time_unit = q.get('timeUnit') if len(q.get('timeUnit')) > 0 else "months"
#         return f" ({q.get('experience')} {time_unit})"
#     else:
#         return ""

# def get_skills_text(dict_arr, key='text'):
#     if dict_arr is not None:
#         return [f"{x.get(key, '')}{get_skills_experience(x)}" for x in dict_arr if len(x.get(key, '')) > 0]
#     else:
#         return []
    
# def get_license_certification_title(dict_arr, key='title'):
#     if dict_arr is not None:
#         return [f"{x.get(key, '')}" for x in dict_arr if len(x.get(key, '')) > 0]
#     else:
#         return []
    
# def format_date_string(datestr_yyyy_mm):
#     date = datetime.datetime.strptime(datestr_yyyy_mm, '%Y-%m')
#     return datetime.datetime.strftime(date, "%B %Y")

# def format_experience_date(date):
#     try:
#         if date.lower() == 'current':
#             return "Present"
#         else:
#             return format_date_string(date)
#     except Exception:
#         return ""

# def format_experience_dates(dates):
#     return f"{format_experience_date(dates.get('startDate'))} - {format_experience_date(dates.get('endDate'))}"

# def make_experience_string(experiences) -> str:
#     result = []
#     try:
#         for exp in experiences:
#             arr = [exp.get('title'), exp.get('company'), format_experience_date(exp.get('dates')),  exp.get('description')]
#             str = "\n".join([s for s in arr if s is not None and len(s) > 0])
#             if len(str) > 0:
#                 result.append(str)
#     except: pass
#     if len(result) > 0:
#         return "\n\n".join(result)
#     return None

# def make_education_string(education) -> str:
#     result = []
#     try:
#         for edu in education:
#             deg_str = " ".join(edu.get('degrees'))
#             arr = [deg_str, edu.get('school')]
#             str = "\n".join([s for s in arr if s is not None and len(s) > 0])
#             if len(str) > 0:
#                 result.append(str)
#     except: pass
#     if len(result) > 0:
#         return "\n\n".join(result)
#     return None

# def make_certifications_licenses_string(row, key):
#     arr = get_license_certification_title(row[f'jsResume{key}'])
#     string = ", ".join([s for s in arr if s is not None and len(s) > 0])
#     return string if len(string)>0 else None

# def make_data(row):
#     header_arr = [row['jsResumeHeadline'], str(row['jsResumeSummary'] or '') + str(row['jsResumeAdditionalInfo'] or '')]
#     header_arr2 = [s for s in header_arr if s is not None and len(s) > 0]
#     header = '\n'.join(header_arr2) if len(header_arr2)>0 else None

#     experience = make_experience_string(row['jsResumeWorkExperience'])
#     education = make_education_string(row['jsResumeEducation'])
    
#     skills_arr = get_skills_text(row['jsResumeSkills'])
#     skills = ", ".join([s for s in skills_arr if s is not None and len(s) > 0])

#     certifications = make_certifications_licenses_string(row, "Certifications")
#     licenses = make_certifications_licenses_string(row, "Licenses")
#     return f"""
# ***JS Resume***\n
# ****Resume Header****
# {header}

# ****Resume Experience****
# {experience}

# ****Education****
# {education}

# ****Skills****
# {skills}

# ****Certifications****
# {certifications}

# ****Licenses****
# {licenses}

# ***JS Activity***\n
# ****Applied Job Titles****
# {row['jsAppliedJobTitles']}

# ****Applied Occupations****
# {row['jsAppliedOccupations']}

# ****Clicked Job Titles****
# {row['jsClickedJobTitles']}

# ****Clicked Occupations****
# {row['jsClickedOccupations']}

# ****Searches****
# {row['jsSearchQueries']}
# """

def make_initial_prompt(row):
    return [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_instruction_single + row['resume_data_combined']}
    ]

def get_gpt_completion(messages, model="gpt-4o-2024-05-13"):
    t0=time.time()
    # print("input token size:", num_tokens_from_messages(messages, model='gpt-3.5-turbo-0613'))
    response = openai.chat.completions.create(
        model=model,
        # response_format={ "type": "json_object" },
        seed=7,
        messages=messages,
        temperature=0
    )
    output = response.choices[0].message.content
    # print('token usage:',response.usage.total_tokens, 'time spent(s):',round(time.time()-t0,2))
    return output


system_instruction = """You are a career advancement expert with specialized knowledge in analyzing job seeker (JS) data to predict career progression. Given a job seeker's resume data and past activity on a job site, your task is to generate a list of 5 to 10 job titles that the jobseeker is likely to advance toward in the next 18 months of their career. 
Follow these guidelines:

**Guidelines:**
- Consider common career trajectories for individuals with similar backgrounds when generating the job titles. These titles should be plausible next steps in the job seeker's career progression.
- The suggested job titles should be loosely based on the job seeker’s previous experiences, reflecting roles they may have held or closely related ones.
- Align the suggested job titles with the jobseeker’s current experience level, avoiding significant jumps in seniority.
- If JS data for a particular field is missing, prioritize the other available fields.
- Give less weight to fields such as education, licenses, and certifications compared to resume experience and past applies.
- If there is a conflict between the resume details and recent activity, prioritize past applies as they are more likely to reflect the jobseeker’s current intentions.
- Ensure the list covers a range of job titles, including some that align closely with past roles and others that represent potential career advancements or shifts.
- Consider job market trends and demand when generating the list of job titles.

*Response Format:**
Provide your evaluation in JSON format, using the following structure-
```
    [
     {
       "title": "Job Title 1",
       "justification": "Brief explanation of how this title aligns with the jobseeker's data."
     },
     {
       "title": "Job Title 2",
       "justification": "Brief explanation of how this title aligns with the jobseeker's data."
     },
     ...
    ]
```
"""

user_instruction_single = """Using the below job seeker(JS) resume and activity data, generate a list of 5 to 10 job titles that the jobseeker is likely to advance toward in the next 18 months of their career:\n
"""

# df = pd.read_csv('js_data_sample.tsv', sep='\t')



openai.base_url = 'https://llm-proxy.sandbox.indeed.net/openai/v1/'
openai.api_key  = st.secrets["openai_api_key"]
openai.organization = 'org-SFf9IpnK1hAwQf3Aq1oa7k90'

# For usage within any official Indeed application. Add PII moderation header
openai.default_headers = {}
openai.default_headers.update({"x-indeed-app": "mrp-rm-explore-match-labeler"})
openai.default_headers.update({"x-indeed-moderation": "both"})

# # Sample data (replace with your actual data)
# data = {
#     'jobseeker_id': [1, 2, 3],
#     'resume_summary': [
#         "Experienced Data Scientist with a demonstrated history of working in the tech industry.",
#         "Marketing specialist with 5 years of experience in digital marketing and brand management.",
#         "Software engineer with expertise in Python, Java, and cloud technologies."
#     ],
#     'experience': [
#         "Data Scientist at XYZ Corp, Analyst at ABC Ltd.",
#         "Marketing Specialist at DEF Inc., Brand Manager at GHI Ltd.",
#         "Software Engineer at JKL Pvt. Ltd., DevOps Engineer at MNO Inc."
#     ],
#     'past_activity': [
#         "Applied to Data Scientist roles, clicked on Machine Learning Engineer jobs.",
#         "Applied to Digital Marketing roles, searched for Social Media Manager jobs.",
#         "Clicked on Backend Developer jobs, applied to Cloud Engineer positions."
#     ]
# }

# # Convert the data to a pandas DataFrame
# df = pd.DataFrame(data)

# # Sample JSON object with relevant job titles (replace with your actual JSON data)
# job_titles_json = """
# {
#     "1": ["Machine Learning Engineer", "AI Researcher", "Data Engineer"],
#     "2": ["Social Media Manager", "Content Strategist", "SEO Specialist"],
#     "3": ["Cloud Architect", "Full Stack Developer", "DevOps Engineer"]
# }
# """

# # Parse the JSON object
# job_titles = json.loads(job_titles_json)

# # Function to generate job titles based on jobseeker_id
# def generate_job_titles(jobseeker_id):
#     return job_titles[str(jobseeker_id)]

# Streamlit app
def main():
    st.sidebar.title("Jobseeker")

    df = pd.read_csv('js_data_sample.parquet')
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
        messages = make_initial_prompt(jobseeker_info)
        relevant_titles = get_gpt_completion(messages, model="gpt-4o-mini-2024-07-18")
        st.subheader("Relevant Job Titles")
        st.write(relevant_titles)

if __name__ == "__main__":
    main()
