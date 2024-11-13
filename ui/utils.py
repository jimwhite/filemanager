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

def log_error(message):
    with open("error.log", "a") as log_file:
        log_file.write(f"{message}\n")

def delete_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        log_error(f"Error deleting file {file_path}: {e}")

def move_file(src, dst):
    try:
        os.rename(src, dst)
    except Exception as e:
        log_error(f"Error moving file from {src} to {dst}: {e}")

def copy_file(src, dst):
    try:
        with open(src, "rb") as fsrc:
            with open(dst, "wb") as fdst:
                while True:
                    buf = fsrc.read(4096)
                    if not buf:
                        break
                    fdst.write(buf)
    except Exception as e:
        log_error(f"Error copying file from {src} to {dst}: {e}")

def create_directory(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        log_error(f"Error creating directory {directory}: {e}")

def delete_directory(directory):
    try:
        os.rmdir(directory)
    except Exception as e:
        log_error(f"Error deleting directory {directory}: {e}")

def list_directories(directory):
    try:
        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                yield os.path.join(root, dir)
    except Exception as e:
        log_error(f"Error listing directories: {e}")
