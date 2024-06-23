import os
import logging
from data_extractor import extract_data_from_pdf
from db_connection import connect_to_db
from data_inserter import insert_data_into_db

def main():
    connection = connect_to_db()
    if not connection:
        logging.error("Failed to connect to the database.")
        print("Failed to connect to the database.")
        return

    pdf_folder = "./pdf_statements"
    for file_name in os.listdir(pdf_folder):
        if file_name.endswith(".pdf") or file_name.endswith(".PDF"):
            file_path = os.path.join(pdf_folder, file_name)
            try:
                data = extract_data_from_pdf(file_path)
                if data:
                    insert_data_into_db(file_name, data, connection)
                else:
                    logging.error(f"No data extracted from {file_name}.")
                    print(f"No data extracted from {file_name}.")
            except Exception as e:
                logging.error(f"Failed to process {file_name}: {e}")
                print(f"Failed to process {file_name}: {e}")

    connection.close()

if __name__ == "__main__":
    main()
