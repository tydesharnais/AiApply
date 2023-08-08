#!/usr/bin/env python

import streamlit as st
import openai as ai
from PyPDF2 import PdfReader

# ai.api_key = st.secrets["openai_key"]
ai.api_key = st.secrets["openai_key"]


st.markdown("""
# 📝 BASED Resume Writer by TyBeats
            
## Gonna be up tremendously after this one ~
Generate a cover letter. All you need to do is:
1. Upload your resume or copy your resume/experiences
2. Paste a relevant job description
3. Input some other relevant user/job data
4. Profit.
"""
)

# radio for upload or copy paste option         
res_format = st.radio(
    "Do you want to upload or paste your resume/key experience",
    ('Upload', 'Paste'))

if res_format == 'Upload':
    # upload_resume
    res_file = st.file_uploader('📁 Upload your resume in pdf format')
    if res_file:
        pdf_reader = PdfReader(res_file)

        # Collect text from pdf
        res_text = ""
        for page in pdf_reader.pages:
            res_text += page.extract_text()
else:
    # use the pasted contents instead
    res_text = st.text_input('Pasted resume elements')

with st.form('input_form'):
    # other inputs
    job_desc = st.text_input('Pasted job description')
    role = st.text_input('Job title/role')
    ai_temp = st.number_input('AI Temperature (0.0-1.0) Input how creative the API can be',value=.99)

    # submit button
    submitted = st.form_submit_button("Generate Resume and Recommendations")

# if the form is submitted run the openai completion   
if submitted:

    # note that the ChatCompletion is used as it was found to be more effective to produce good results
    # using just Completion often resulted in exceeding token limits
    # according to https://platform.openai.com/docs/models/gpt-3-5
    # Our most capable and cost effective model in the GPT-3.5 family is gpt-3.5-turbo which has been optimized for chat 
    # but works well for traditional completions tasks as well.

    completion = ai.ChatCompletion.create(
      #model="gpt-3.5-turbo-16k", 
      model = "gpt-3.5-turbo",
      temperature=0.99,
      messages = [
        {"role": "user", "content" : f"You will need to rewrite a resume based on keywords you find in a job description to tailor it to get past the ATS hiring system. Tailor your resume to the job description provided with respect to the job title and skills/qualifications needed."},
        {"role": "user", "content" : f"There are rules to rewriting the resume. I will list the rules below as well as some descriptions for the rules so you get a better understanding."},
         {"role": "user", "content" : f""" 
        Rule 1: Use the top half of the resumes first page.
          Description: Together with your contact information and resume summary, your job description is one of the first things recruiters and hiring managers read in your resume. 
Since they only spend around 7 seconds before they rule you out or move you to the next round, it is imperative that you put your experience section on the top half of your resume.    
        """},
        {"role": "user", "content" : f""" 
        Rule 2: Check the specific job description of the position
         Description: Go line by line through the job description and ask yourself these questions:
        “Does my resume experience section clearly state that I can do what's required of this role?”
        “Am I using the same language found in the job description or job posting?”
        By doing this, you might find several different or missing skills and keywords in your generic resume.     
         """},
         {"role": "user", "content" : f""" 
        Rule 3: Begin with basic details.
          Description: Be specific. The hiring manager should know exactly what you did at your previous or current employers, so they can gain a thorough understanding of your work history. Do not oversimplify the original work experiences but take out what doesn't correlate well with the job that being applied for. 
          Begin each resume job description with essential information about the job and company: your official job title, the name and address of the company, and the period in which you worked there."""},
           {"role": "user", "content" : f""" 
        MOST IMPORTANT Rule 4: Match skills and keywords from the job description
          Description: Mirroring the language, keywords, and buzzwords found within the job description is the easiest way to demonstrate you're a better match than the competition.
            The best way to ensure you pass the ATS is to take words from the job posting and strategically put them in your job descriptions and other resume sections. But make sure you don't stuff your resume with too many keywords.
            """},
        {"role": "user", "content" : f""" 
        Rule 6: Focus on skills and quantify your achievements
          Description: Be selective about what you include. Place an emphasis on your accomplishments over job responsibilities.
         Use numbers and action verbs to describe your role and responsibilities. Action verbs are great at conveying your leadership potential and work well at impressing hiring managers. 
            """},
        {"role": "user", "content" : f""" 
        Rule 7: Do not lie
          Description: Emphasizing or deemphasizing your resume skills is not the same as lying on your resume (which I definitely don't suggest). Few applicants have every skill and meet every qualification.
          Tailoring your resume is about making sure the recruiter or hiring manager notices the ones you do have. Do not list job experiences that have not happened yet.
            """},

        {"role": "user", "content" : f"My resume text: {res_text}"},
        {"role": "user", "content" : f"The job description is: {job_desc}"},
        {"role": "user", "content" : f"The job title/role : {role}"},
        {"role": "user", "content" : f"The resume should have the same format."},
        
        {"role": "user", "content" : f""" 
        note that contact information may be found in the included resume text and use and/or summarize specific resume context for the new resume.
            """},
        {"role": "user", "content" : f"Generate a specific resume based on the original resume and job description based on the above. Generate the response and include appropriate spacing between the paragraph text with respect to the previous resume and the rewriting rules. Rephrase a new summary to appeal to the keywords and main points of the job description. When generating the new specific resume, really tailor it towards the job description without taking away any skills of the original resume."},
        {"role": "user", "content" : f"""Finally based on the original resume, based on your analysis of the given resume and the job description, give an opinion of 1. What is likelihood of getting an interview with this company? Give a percentage of how well the original resume correlated to the job description and give a percentage of how well the new resume correlates to the job description.
         2. What did you change/remove and why? 
         3. What is the most important parts of the job description?
         Format this answer as 3 lines below the updated resume as 
         Likelihood of Interview: (your answer)
         Original Resume Correlation: (your answer)
         Updated Resume Correlation: (your answer)
         What I changed: (your answer)
         Most important keywords/parts of the job description: (your answer)"""}
      ]
    )

    response_out = completion['choices'][0]['message']['content']
    st.write(response_out)

    # include an option to download a txt file
    st.download_button('Download the Resume', response_out,file_name=f'{role}_ResumeTweaks.txt')

    st.info('Resume Successfully downloaded')

st.markdown("""
# 📝 BASED Cover Letter Writer by TyBeats
            
## Gonna be up expediously after this one ~
Generate a cover letter. All you need to do is:
1. Upload your resume or copy your resume/experiences
2. Paste a relevant job description
3. Input some other relevant user/job data
"""
)

with st.form('cover_form'):
    st.write('Fill in theese forms below')
    job_desc = st.text_input('Pasted job description')


    user_name = st.text_input('Your name')
    company = st.text_input('Company name')
    manager = st.text_input('Hiring manager')
    role = st.text_input('Job title/role')
    referral = st.text_input('How did you find out about this opportunity?')
    ai_temp = st.number_input('AI Temperature (0.0-1.0) Input how creative the API can be',value=.99)

    # submit button
    submitted_Cover = st.form_submit_button("Generate Cover Letter")

# if the form is submitted run the openai completion   
if submitted_Cover:

    # note that the ChatCompletion is used as it was found to be more effective to produce good results
    # using just Completion often resulted in exceeding token limits
    # according to https://platform.openai.com/docs/models/gpt-3-5
    # Our most capable and cost effective model in the GPT-3.5 family is gpt-3.5-turbo which has been optimized for chat 
    # but works well for traditional completions tasks as well.

    completion = ai.ChatCompletion.create(
      #model="gpt-3.5-turbo-16k", 
      model = "gpt-3.5-turbo",
      temperature=ai_temp,
      messages = [
        {"role": "user", "content" : f"You will need to generate a cover letter based on specific resume and a job description"},
        {"role": "user", "content" : f"My resume text: {res_text}"},
        {"role": "user", "content" : f"The job description is: {job_desc}"},
        {"role": "user", "content" : f"The candidate's name to include on the cover letter: {user_name}"},
        {"role": "user", "content" : f"The job title/role : {role}"},
        {"role": "user", "content" : f"The hiring manager is: {manager}"},
        {"role": "user", "content" : f"How you heard about the opportunity: {referral}"},
        {"role": "user", "content" : f"The company to which you are generating the cover letter for: {company}"},
        {"role": "user", "content" : f"The cover letter should have three content paragraphs"},
        {"role": "user", "content" : f""" 
        In the first paragraph focus on the following: you will convey who you are, what position you are interested in, and where you heard
        about it, and summarize what you have to offer based on the above resume
        """},
            {"role": "user", "content" : f""" 
        In the second paragraph focus on why the candidate is a great fit drawing parallels between the experience included in the resume 
        and the qualifications on the job description.
        """},
                {"role": "user", "content" : f""" 
        In the 3RD PARAGRAPH: Conclusion
        Restate your interest in the organization and/or job and summarize what you have to offer and thank the reader for their time and consideration.
        """},
        {"role": "user", "content" : f""" 
        note that contact information may be found in the included resume text and use and/or summarize specific resume context for the letter
            """},
        {"role": "user", "content" : f"Use {user_name} as the candidate"},
        
        {"role": "user", "content" : f"Generate a specific cover letter based on the above. Generate the response and include appropriate spacing between the paragraph text"}
      ]
    )

    response_out = completion['choices'][0]['message']['content']
    st.write(response_out)

    # include an option to download a txt file
    st.download_button('Download the cover_letter', response_out, file_name=f'{company}_CoverLetter.txt')
