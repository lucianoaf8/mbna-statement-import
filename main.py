import logging
from db_connection import connect_to_db
from file_loader import load_files
from data_extractor import extract_data_from_pdf
from data_inserter import insert_data_into_db

# Set up logging
log_file_path = './logs/pdf_to_db.log'
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def main():
    connection = connect_to_db()
    if not connection:
        logging.error("Failed to connect to the database.")
        print("Failed to connect to the database.")
        return

    pdf_folder = "./pdf_statements"
    files = load_files(pdf_folder)
    
    for file_path in files:
        try:
            data = extract_data_from_pdf(file_path)
            if data:
                insert_data_into_db(file_path, data, connection)
        except Exception as e:
            logging.error(f"Failed to process {file_path}: {e}")
            print(f"Failed to process {file_path}: {e}")
    
    connection.close()

if __name__ == "__main__":
    main()
