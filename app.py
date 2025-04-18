import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="MBBS Exam Analyzer", layout="wide")

# Title and instructions
st.title("🧠 MBBS Exam Question Analyzer (Open Source)")

# Upload section
st.subheader("📤 Upload Your Question Paper")
college = st.text_input("Enter your College Name")
subject = st.text_input("Enter Subject")
year = st.text_input("Enter Year")
uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file and college and subject and year:
    folder = f"user_uploads/{college}/{subject}"
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{year}.{uploaded_file.name.split('.')[-1]}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ Uploaded successfully! It will be analyzed and added.")

# View section
st.subheader("📊 View Most Asked Questions")

if os.path.exists("all_questions.csv"):
    df = pd.read_csv("all_questions.csv")
    col_option = st.selectbox("Select College", sorted(df["College"].unique()))
    sub_option = st.selectbox("Select Subject", sorted(df["Subject"].unique()))
    filtered = df[(df["College"] == col_option) & (df["Subject"] == sub_option)]
    top_questions = filtered["Question"].value_counts().head(10)
    st.write("Top 10 Frequently Asked Questions:")
    st.table(top_questions)
else:
    st.warning("No data found. Please upload papers first.")

import streamlit as st
import pandas as pd

st.title("MBBS Question Analyzer")

try:
    df = pd.read_csv("all_questions.csv")
    st.success("CSV file loaded successfully!")
    st.dataframe(df)
except Exception as e:
    st.error(f"Error loading file: {e}")
