import PyPDF2
import logging

def extract_data_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            number_of_pages = len(reader.pages)
            text = ""
            for page_number in range(number_of_pages):
                page = reader.pages[page_number]
                try:
                    page_text = page.extract_text() if page.extract_text() else ""
                    text += page_text
                    logging.debug(f"Extracted text from page {page_number}: {page_text}")
                    print(f"Extracted text from page {page_number}: {page_text}")
                except Exception as e:
                    logging.warning(f"Error reading page {page_number} in file {file_path}: {e}")
                    print(f"Error reading page {page_number} in file {file_path}: {e}")
                    continue
        
        # Log full extracted text for debugging
        logging.debug(f"Full extracted text from PDF: {text}")
        print(f"Full extracted text from PDF: {text}")

        return text
    except Exception as e:
        logging.error(f"Error extracting data from PDF {file_path}: {e}")
        print(f"Error extracting data from PDF {file_path}: {e}")
        raise
