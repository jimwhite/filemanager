import hashlib
import os

def compute_md5sum(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error computing md5sum: {e}")
        return None

def list_files(directory):
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                yield os.path.join(root, file)
    except Exception as e:
        print(f"Error listing files: {e}")

def is_duplicate(file_path, db):
    md5sum = compute_md5sum(file_path)
    if not md5sum:
        return False
    result = db.query_file(file_path)
    return result is not None and result[0] == md5sum
