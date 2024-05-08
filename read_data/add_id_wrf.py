import json
import os
import gzip  # Import the gzip module for handling .json.gz files
from multiprocessing import Pool, Value, Lock, Manager
from typing import Tuple

def initialize_counter(lock, start_value):
    """
    Initializes a global counter and lock for use in the worker function.
    """
    global counter
    global counter_lock
    counter = start_value
    counter_lock = lock

def process_file(args: Tuple[str, str, Value, Lock]):
    """
    Processes a single .json.gz file by adding a unique ID to each JSON object (as a string) and writes it to a new folder.
    Receives a tuple containing file_path, dest_folder, and a shared counter with a lock.
    """
    file_path, dest_folder = args
    try:
        updated_json_lines = []
        
        # Use gzip.open for reading .json.gz files
        with gzip.open(file_path, 'rt', encoding='utf-8') as file:
            for line in file:
                json_obj = json.loads(line)
                
                with counter_lock:
                    # Convert the counter value to a string before assigning it as an ID
                    json_obj['id'] = str(counter.value)
                    counter.value += 1
                
                updated_json_lines.append(json_obj)

        # Adjust the destination file path to also be .json.gz
        dest_file_name = os.path.basename(file_path)
        dest_file_path = os.path.join(dest_folder, dest_file_name)

        # Use gzip.open with 'wt' to write compressed JSON lines
        with gzip.open(dest_file_path, 'wt', encoding='utf-8') as file:
            for obj in updated_json_lines:
                file.write(json.dumps(obj) + '\n')

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_files_in_folder(src_folder_path: str, dest_folder_path: str, num_processes: int = 32):
    """
    Processes all .json.gz files in a source folder and writes them to a destination folder using multiprocessing Pool.
    """
    if not os.path.exists(dest_folder_path):
        os.makedirs(dest_folder_path)  # Create the destination folder if it doesn't exist

    files = [os.path.join(src_folder_path, f) for f in os.listdir(src_folder_path) if f.endswith('.json.gz')]

    # Prepare shared counter and lock
    manager = Manager()
    start_id = manager.Value('i', 0)
    lock = manager.Lock()

    # Update here: Ensure pool_args only contains tuples of (file_path, dest_folder)
    pool_args = [(file_path, dest_folder_path) for file_path in files]

    # Initialize Pool with the counter and lock
    with Pool(processes=num_processes, initializer=initialize_counter, initargs=(lock, start_id)) as pool:
        pool.map(process_file, pool_args)


if __name__ == "__main__":
    #src_folder_path = '/home/xundong/data/Arxiv/documents1/'  # Update this to your source folder path
    src_folder_path = '/home/wrf1/dolma/wikipedia/v0/documents_no_id/redpajamaarxiv/'  # Update this to your source folder path
    dest_folder_path = '/home/wrf1/dolma/wikipedia/v0/documents/'  # Update this to your destination folder path
    process_files_in_folder(src_folder_path, dest_folder_path)
