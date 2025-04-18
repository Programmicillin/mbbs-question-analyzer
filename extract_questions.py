import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import pandas as pd

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text

data = []

# CHANGE THIS IF YOUR PAPERS FOLDER IS IN A DIFFERENT PLACE
root_dir = os.path.expanduser("~/Desktop/papers")

for root, _, files in os.walk(root_dir):
    for file in files:
        file_path = os.path.join(root, file)
        if file.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file.endswith((".jpg", ".jpeg", ".png")):
            text = extract_text_from_image(file_path)
        else:
            continue

        questions = [q.strip().replace("\n", " ") + "?" for q in text.split("?") if len(q.strip()) > 15]

        try:
            year = file.split(".")[0]
            subject = os.path.basename(os.path.dirname(file_path))
            college = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
        except:
            college, subject, year = "Unknown", "Unknown", "Unknown"

        for q in questions:
            data.append({
                "College": college,
                "Subject": subject,
                "Year": year,
                "Question": q
            })

df = pd.DataFrame(data)
df.to_csv("all_questions.csv", index=False)
print("✅ Extracted and saved to all_questions.csv")
