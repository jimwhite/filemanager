# filemanager

## File Manager (fm) CLI App

The `fm` app is a Python CLI file-manager that allows you to search a file system or a sub-directory, compute the md5sum for each file, and save the file path and md5sum to a SQLite database. The app also allows you to search the database for a file path and return the md5sum.

### Requirements

- Python 3.x
- SQLite

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/jimwhite/filemanager.git
   cd filemanager
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Usage

The `fm` app supports the following actions:

- `add`: Recursively scan a directory and compute the md5sum for each file, then store the md5sum and the path into the database. If a file already has the same md5sum in the database, print a message and return an exit code of 1.
- `add1`: Compute the md5sum for a single file and store the md5sum and the path into the database. If a file with the same md5sum is already in the database, print a message and return an exit code of 1.
- `check`: Provide a list of duplicates. For each md5sum with more than one path, show the sum and the paths.
- `dedup`: Like `check`, but for each duplicate path, prompt the user whether to delete it.

### Examples

1. Add a directory to the database:
   ```sh
   python fm.py add /path/to/directory
   ```

2. Add a single file to the database:
   ```sh
   python fm.py add1 /path/to/file
   ```

3. Check for duplicate files:
   ```sh
   python fm.py check
   ```

4. Deduplicate files:
   ```sh
   python fm.py dedup
   ```

### License

This project is licensed under the GNU Affero General Public License - see the [LICENSE](LICENSE) file for details.
