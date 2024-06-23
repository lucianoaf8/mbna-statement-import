import os

def load_files(pdf_folder):
    return [os.path.join(pdf_folder, file_name) for file_name in os.listdir(pdf_folder) if file_name.endswith(".pdf") or file_name.endswith(".PDF")]
