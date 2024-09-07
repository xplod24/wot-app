import os
import hashlib
import json

# Function to get the checksum from the filetree file
def get_checksum_from_filetree(filename, filetree_file):
    with open(filetree_file, 'r') as f:
        for line in f:
            file, checksum = line.strip().split()
            if file == filename:
                return checksum
    return None

# Function to create the filetree file
def create_filetree(download_dir, filetree_file):
    with open(filetree_file, 'w') as f:
        for root, dirs, files in os.walk(download_dir):
            for file in files:
                filepath = os.path.join(root, file)
                with open(filepath, 'rb') as f2:
                    file_checksum = hashlib.md5(f2.read()).hexdigest()
                f.write(f"{file} {file_checksum}\n")