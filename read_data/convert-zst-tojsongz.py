import json
import zstandard as zstd
import gzip
import os

def convert_zst_to_json_gz(zst_folder_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    
    # Iterate over all files in the folder
    for filename in os.listdir(zst_folder_path):
        json_data = []
        if filename.startswith("chunk_") and filename.endswith(".jsonl.zst"):
            zst_file_path = os.path.join(zst_folder_path, filename)
            # Extract the chunk number from the filename
            chunk_number = filename.split("_")[1].split(".")[0]
            

            # Open zst file
            with open(zst_file_path, 'rb') as zst_file:
                # Create zstd decompressor
                dctx = zstd.ZstdDecompressor()
                # Read the entire content of the zst file
                zst_content = dctx.decompress(zst_file.read())

                # Split the content by lines and parse JSON
            for line in zst_content.decode('utf-8').splitlines():
                json_data.append(json.loads(line))
                

                # Create a new json.gz file for writing
                json_gz_file_path = os.path.join(output_folder, f"chunk_{chunk_number}.json.gz")

        print_data = json_data[:1]
        print(print_data)
        print("The chunk number is:", chunk_number)
    
        with gzip.open(json_gz_file_path, 'wt', compresslevel=9) as json_gz_file:
                # Split the content by lines and parse JSON
            for line in zst_content.decode('utf-8').splitlines():
                json.dump(json.loads(line), json_gz_file)
                json_gz_file.write('\n')



# Specify the folder containing zst files and the output folder
zst_folder_path = '/mnt/geogpt-gpfs/llm-course/public/datasets/RedPajamaStackExchange'
output_folder = '/home/wrf1/OLMo/test_fixtures_redpajamastackexchange'


# Convert zst files to JSON and compress them into .json.gz files
convert_zst_to_json_gz(zst_folder_path, output_folder)
