from pypdf import PdfReader
import os
import streamlit as st
import anthropic
from dotenv import load_dotenv

load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Client(api_key=anthropic_api_key)

MODEL_NAME = "claude-3-opus-20240229"

st.title("Resume Editor with Claude Opus")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    def get_completion(client, prompt):
        return client.messages.create(
            model=MODEL_NAME,
            max_tokens=4096,
            messages=[{
                "role": 'user', "content": prompt
            }]
        ).content[0].text

    completion = get_completion(client,
                                f"""Here is a resume: <resume>{text}</resume>

Please do the following:

1. Ask clarifying questions to understand their background, experience, career goals, and any specific requirements for their desired roles.
2. Provide tailored advice on structuring and formatting their resume based on their situation, including section order, content suggestions, keyword optimization, and formatting tips.
3. Recommend strategies for highlighting their most relevant skills, achievements, and experiences in a concise and compelling way that aligns with what employers are seeking.
4. Offer guidance on ensuring consistency in areas like date formatting, tenses, personal pronouns usage, and writing style throughout the resume.
5. Suggest ways to make their resume accomplishments-driven by using quantifiable metrics, hard numbers, and concrete examples wherever possible.
6. Give feedback on refining their professional summary or resume objective statement to immediately capture an employer's attention.
7. Generate a fully edited version of the resume that incorporates all your suggestions and feedback.

Your response should be constructive, insightful, and designed to help the user elevate the quality of their writing. Please provide the fully edited resume as the final output.
""")

    
    st.write(completion)



  





