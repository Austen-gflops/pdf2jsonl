import streamlit as st
import fitz  # PyMuPDF
import json
import base64
import zipfile
import os
import datetime

def process_pdf(file):
    with fitz.open(stream=file.stream) as doc:
        text = [page.get_text() for page in doc]
    return text

def create_jsonl(content, filename):
    jsonl_data = ""
    for page, text in enumerate(content):
        if text:
            jsonl_data += json.dumps({"page": page + 1, "text": text}) + "\n"
    with open(filename, 'w') as f:
        f.write(jsonl_data)

def create_zip(files):
    zip_filename = f'{datetime.datetime.now().strftime("%Y-%m-%d")}.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files:
            zipf.write(file)
            os.remove(file)  # Remove the file after adding it to the zip
    return zip_filename

def download_link(file_path):
    with open(file_path, "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/zip;base64,{b64}" download="{os.path.basename(file_path)}">Click here to download the files</a>'
        return href

def main():
    st.title("PDF to JSONL Converter")
    
    uploaded_files = st.file_uploader("Upload PDF Files", accept_multiple_files=True, type="pdf")
    if uploaded_files:
        jsonl_files = []
        for file in uploaded_files:
            content = process_pdf(file)
            jsonl_filename = f"{file.name}.jsonl"
            create_jsonl(content, jsonl_filename)
            jsonl_files.append(jsonl_filename)

        if jsonl_files:
            zip_filename = create_zip(jsonl_files)
            st.markdown(download_link(zip_filename), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
