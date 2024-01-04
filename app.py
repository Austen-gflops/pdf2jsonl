import streamlit as st
import fitz  # PyMuPDF
import json
import base64
import os
import datetime

def process_pdf(file):
    with fitz.open("pdf", file.getvalue()) as doc:  # Open the PDF directly from bytes
        text = [page.get_text() for page in doc]
    return text

def append_to_jsonl(content, file_name, jsonl_data):
    for page, text in enumerate(content):
        if text:
            # Append data to the jsonl_data string
            jsonl_data += json.dumps({"file_name": file_name, "page": page + 1, "text": text}, ensure_ascii=False) + "\n"
    return jsonl_data

def download_link(object_to_download, download_filename, download_link_text):
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def main():
    st.title("PDF to JSONL Converter")
    
    uploaded_files = st.file_uploader("Upload PDF Files", accept_multiple_files=True, type="pdf")
    if uploaded_files:
        combined_jsonl_data = ""
        for file in uploaded_files:
            content = process_pdf(file)
            combined_jsonl_data = append_to_jsonl(content, file.name, combined_jsonl_data)

        if combined_jsonl_data:
            today_date = datetime.datetime.now().strftime("%Y-%m-%d")
            jsonl_filename = f"{today_date}.jsonl"
            st.markdown(download_link(combined_jsonl_data, jsonl_filename, "Click here to download your JSONL file"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
