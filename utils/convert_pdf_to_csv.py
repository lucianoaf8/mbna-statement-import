import pdfplumber
import pandas as pd
import os

def convert_pdf_to_csv(pdf_path, csv_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)

    # Join all text and split by new lines
    text_data = "\n".join(all_text).split('\n')

    # Create a DataFrame from the text data
    df = pd.DataFrame(text_data, columns=["text"])
    df.to_csv(csv_path, index=False)
    print(f"PDF converted to CSV and saved at {csv_path}")
