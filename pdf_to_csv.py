import pdfplumber
import pandas as pd

# Path to the PDF file
pdf_path = "pdf_statements/Amazon_23May2024.PDF"

# Function to extract data from a specific section
def extract_section(text, start_phrase, end_phrase):
    start_index = text.find(start_phrase)
    end_index = text.find(end_phrase, start_index)
    return text[start_index:end_index].strip()

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    all_text = []
    for page in pdf.pages:
        # Extract text from each page
        text = page.extract_text()
        if text:
            all_text.append(text)

# Join all text from all pages
full_text = "\n".join(all_text)

# Extract specific sections
payment_info = extract_section(full_text, "Payment information", "Summary of your account")
account_summary = extract_section(full_text, "Summary of your account", "Details of your transactions")
transaction_details = extract_section(full_text, "Details of your transactions", "Important Notice(s)")

# Save each section to a separate text file
with open("extracted_files/payment_info.txt", "w") as file:
    file.write(payment_info)

with open("extracted_files/account_summary.txt", "w") as file:
    file.write(account_summary)

with open("extracted_files/transaction_details.txt", "w") as file:
    file.write(transaction_details)

# Function to parse a section into a structured DataFrame
def parse_section(section_text):
    lines = section_text.split("\n")
    data = [line.split() for line in lines]
    return pd.DataFrame(data)

# Parse sections into DataFrames
df_payment_info = parse_section(payment_info)
df_account_summary = parse_section(account_summary)
df_transaction_details = parse_section(transaction_details)

# Save DataFrames to CSV files
df_payment_info.to_csv("extracted_files/payment_info.csv", index=False, header=False)
df_account_summary.to_csv("extracted_files/account_summary.csv", index=False, header=False)
df_transaction_details.to_csv("extracted_files/transaction_details.csv", index=False, header=False)

print("Extraction and structuring complete. The sections have been saved as separate text and CSV files.")
