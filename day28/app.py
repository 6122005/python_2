import streamlit as st

st.set_page_config(

    page_title="PDF AI",

    page_icon="📄",

    layout="wide"

)

st.title("📄 PDF AI Assistant")

st.write(
    "Upload your PDF and ask any question."
)

st.divider()

uploaded_file = st.file_uploader(

    "Choose PDF",

    type=["pdf"]

)

if uploaded_file:

    st.success("PDF Uploaded Successfully")

    st.write("File Name:", uploaded_file.name)

    st.write("Size:", uploaded_file.size, "bytes")

question = st.text_input(

    "Ask your Question"

)

if st.button("Ask"):

    if uploaded_file is None:

        st.error("Please Upload PDF")

    elif question == "":

        st.warning("Please Enter Question")

    else:

        st.success("Everything is Ready")

        st.write("Question :", question)

with st.sidebar:

    st.header("About")

    st.write("Week 6 - Day 28")

    st.write("First Streamlit Application")