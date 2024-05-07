import gzip
import json
import os

def read_json_file(file_path, keep_original=False):
    # Check if the file is a .json.gz file
    if file_path.endswith('.json.gz'):
        # Generate the unzipped file name
        unzipped_file = os.path.splitext(file_path)[0]
        with gzip.open(file_path, 'rb') as f_in:
            with open(unzipped_file, 'wb') as f_out:
                f_out.write(f_in.read())
        file_path = unzipped_file

    # Open the file
    with open(file_path, "r") as file:
        # Read the first two lines
        for i in range(1):
            line = file.readline()
            print(line)

    # Remove the unzipped file if required and the file is .json.gz
    if not keep_original and file_path.endswith('.json.gz'):
        os.remove(unzipped_file)
    # Check if the file is a .json file
    elif file_path.endswith('.json'):
        # Re-open the file to read again
        with open(file_path, "r") as file:
            # Read the first two lines
            for i in range(2):
                line = file.readline()
                print(line)

# Call the function and provide the file path
read_json_file("/home/wrf1/1data/pes2o/pes2o_v2-0020.json", keep_original=True)

