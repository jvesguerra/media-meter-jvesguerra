import os
import pandas as pd
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pymongo import MongoClient, UpdateOne
from datetime import datetime
import shutil
from pathlib import Path

# Configuration
WATCH_DIR = "../api/storage/app/medalists/"
ARCHIVE_DIR = "storage/app/medalists/archive/"
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "database"
COLLECTION_NAME = "medalists"

# Logger setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

collection.create_index("name", unique=True) #  indexing key fields in MongoDB for faster queries and check uniqueness

# Handler for monitoring directory
# If file is created and is a csv file, it is processed
class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"): 
            process_csv(event.src_path)

# Process CSV file
def process_csv(file_path):
    logging.info(f"Processing file: {file_path}")
    try:
        # read CSV
        df = pd.read_csv(file_path)

        # Insert into MongoDB
        operations = []
        for _, row in df.iterrows():
            operations.append(
                UpdateOne(
                    {"name": row["name"]},
                    {"$set": row.to_dict()},
                    upsert=True
                )
            )
        if operations:
            result = collection.bulk_write(operations)
            logging.info(f" Upload Success, Inserted: {result.upserted_count}, Updated: {result.modified_count}")
        else:
            logging.info(f"Upload Failed")
            

        # Archive file
        archive_path = os.path.join(ARCHIVE_DIR, os.path.basename(file_path))
        shutil.move(file_path, archive_path)
        logging.info(f"File archived to: {archive_path}")

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")

# Main service
def monitor_directory():
    os.makedirs(WATCH_DIR, exist_ok=True)
    event_handler = CSVHandler()
    observer = Observer()   #watches WATCH_DIR
    observer.schedule(event_handler, path=WATCH_DIR, recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    logging.info("Starting Python Background Service")
    monitor_directory()
