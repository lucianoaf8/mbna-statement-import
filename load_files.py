import os

def load_files_from_directory(directory):
    pdf_files = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".pdf") or file_name.endswith(".PDF"):
            pdf_files.append(os.path.join(directory, file_name))
    return pdf_files
