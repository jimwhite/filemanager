import os
import hashlib
import sqlite3
import argparse

DB_NAME = 'filemanager.db'

def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (path TEXT PRIMARY KEY, md5sum TEXT)''')
    conn.commit()
    conn.close()

def compute_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def add_directory(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            add_file(file_path)

def add_file(file_path):
    md5sum = compute_md5(file_path)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT path FROM files WHERE md5sum=?", (md5sum,))
    result = c.fetchone()
    if result:
        print(f"File with md5sum {md5sum} already exists in the database.")
        conn.close()
        return 1
    c.execute("INSERT INTO files (path, md5sum) VALUES (?, ?)", (file_path, md5sum))
    conn.commit()
    conn.close()
    return 0

def check_duplicates():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT md5sum, GROUP_CONCAT(path) FROM files GROUP BY md5sum HAVING COUNT(*) > 1")
    duplicates = c.fetchall()
    for md5sum, paths in duplicates:
        print(f"md5sum: {md5sum}")
        for path in paths.split(','):
            print(f"  {path}")
    conn.close()

def dedup():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT md5sum, GROUP_CONCAT(path) FROM files GROUP BY md5sum HAVING COUNT(*) > 1")
    duplicates = c.fetchall()
    for md5sum, paths in duplicates:
        print(f"md5sum: {md5sum}")
        path_list = paths.split(',')
        for path in path_list[1:]:
            response = input(f"Do you want to delete {path}? (y/n): ")
            if response.lower() == 'y':
                os.remove(path)
                c.execute("DELETE FROM files WHERE path=?", (path,))
    conn.commit()
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='File Manager')
    parser.add_argument('action', choices=['add', 'add1', 'check', 'dedup'])
    parser.add_argument('path', nargs='?', help='Path to file or directory')
    args = parser.parse_args()

    create_db()

    if args.action == 'add':
        if args.path:
            add_directory(args.path)
        else:
            print("Please provide a directory path.")
    elif args.action == 'add1':
        if args.path:
            add_file(args.path)
        else:
            print("Please provide a file path.")
    elif args.action == 'check':
        check_duplicates()
    elif args.action == 'dedup':
        dedup()

if __name__ == '__main__':
    main()
