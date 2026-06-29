import streamlit as st

from pdf_rag import process_pdf

from pdf_rag import ask_question


st.set_page_config(

    page_title="AI PDF QA",

    page_icon="📄"

)


st.title("📄 AI PDF Question Answer")


uploaded_file = st.file_uploader(

    "Upload PDF",

    type="pdf"

)


if uploaded_file:

    with open("temp.pdf", "wb") as f:

        f.write(uploaded_file.read())

    st.success("PDF Uploaded Successfully")


    if st.button("Process PDF"):

        with st.spinner("Processing PDF..."):

            process_pdf("temp.pdf")

        st.success("PDF Ready!")


st.divider()


question = st.text_input(

    "Ask a Question"

)


if st.button("Ask"):

    if question == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            answer = ask_question(question)

        st.write("## Answer")

        st.write(answer)