import os
import shutil
import datetime
import hashlib
import getpass
import logging

Set up logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_checksum(file_path):
    """Calculate the checksum of a file"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def backup_files(source_paths, target_dir, encryption_password=None):
    """Backup files and folders"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(target_dir, f"backup_{timestamp}")
    os.makedirs(backup_folder, exist_ok=True)

    for source_path in source_paths:
        if os.path.isfile(source_path):
            backup_file_path = os.path.join(backup_folder, os.path.basename(source_path))
            shutil.copy2(source_path, backup_file_path)
            logging.info(f"File backed up: {source_path}")
            if encryption_password:
                # Encrypt the file using the provided password
                # NOTE: This is a basic example and may not be secure for all use cases
                with open(backup_file_path, 'rb') as f:
                    file_data = f.read()
                encrypted_data = bytes(a ^ b for a, b in zip(file_data, encryption_password.encode()))
                with open(backup_file_path, 'wb') as f:
                    f.write(encrypted_data)
                logging.info(f"File encrypted: {backup_file_path}")
            checksum = calculate_checksum(backup_file_path)
            logging.info(f"Checksum: {checksum}")
            print(f"File backed up: {source_path}")
        elif os.path.isdir(source_path):
            backup_folder_path = os.path.join(backup_folder, os.path.basename(source_path))
            shutil.copytree(source_path, backup_folder_path)
            logging.info(f"Folder backed up: {source_path}")
            print(f"Folder backed up: {source_path}")
        else:
            logging.warning(f"Skipped: {source_path} (not a file or folder)")
            print(f"Skipped: {source_path} (not a file or folder)")

def backup_database(db_path, target_dir, encryption_password=None):
    """Backup database file"""
    if os.path.isfile(db_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(target_dir, f"backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)
        db_backup_path = os.path.join(backup_folder, os.path.basename(db_path))
        shutil.copy2(db_path, db_backup_path)
        logging.info(f"Database backed up: {db_backup_path}")
        if encryption_password:
            # Encrypt the database file using the provided password
            # NOTE: This is a basic example and may not be secure for all use cases
            with open(db_backup_path, 'rb') as f:
                file_data = f.read()
            encrypted_data = bytes(a ^ b for a, b in zip(file_data, encryption_password.encode()))
            with open(db_backup_path, 'wb') as f:
                f.write(encrypted_data)
            logging.info(f"Database encrypted: {db_backup_path}")
        checksum = calculate_checksum(db_backup_path)
        logging.info(f"Checksum: {checksum}")
        print(f"Database backed up: {db_backup_path}")
    else:
        logging.warning(f"Database not found: {db_path}")
        print(f"Database not found: {db_path}")

if __name__ == "__main__":
    target_directory = "/path/to/backup/directory"
    encryption_password = getpass.getpass("Enter encryption password (optional): ")
    if not encryption_password:
        encryption_password = None

    print("Select what you want to back up:")
    print("1. Specific files")
    print("2. Specific folders")
    print("3. Database")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        files_to_backup = input("Enter the full paths of the files to back up (comma-separated): ")
        source_paths = [path.strip() for path in files_to_backup.split(',')]
        backup_files(source_paths, target_directory, encryption_password)
    elif choice == '2':
        folders_to_backup = input("Enter the full paths of the folders to back up (comma-separated): ")
        source_paths = [path.strip() for path in folders_to_backup.split(',')]
        backup_files(source_paths, target_directory, encryption_password)
    elif choice == '3':
        db_path = input("Enter the full path of the database file to back up: ")
        backup_database
```
