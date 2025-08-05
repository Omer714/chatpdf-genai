import streamlit as st
import PyPDF2
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

import openai

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ask_question(prompt, context):
    full_prompt = f"Based on the following PDF content, answer the question:\n\n{context}\n\nQuestion: {prompt}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content


st.title("📄 Chat with your PDF (GenAI Side Project)")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file:
    with st.spinner("Reading PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)

    user_question = st.text_input("Ask a question about the PDF:")
    if user_question:
        with st.spinner("Thinking..."):
            answer = ask_question(user_question, pdf_text[:4000])
            st.write("🧠 Answer:")
            st.write(answer)
