import os
import shutil
import datetime
import hashlib
import getpass
import logging
import smtplib
import zipfile
from cryptography.fernet import Fernet
from pathlib import Path

# Set up logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_key(password):
    """Generate a Fernet key from a password."""
    return Fernet(Fernet.generate_key())

def encrypt_file(file_path, key):
    """Encrypt a file using the provided key."""
    fernet = Fernet(key)
    with open(file_path, 'rb') as f:
        file_data = f.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(file_path, key):
    """Decrypt a file using the provided key."""
    fernet = Fernet(key)
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, 'wb') as f:
        f.write(decrypted_data)

def calculate_checksum(file_path):
    """Calculate the checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compress_backup(backup_folder):
    """Compress the backup folder into a zip file."""
    zip_file_path = f"{backup_folder}.zip"
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(backup_folder):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), backup_folder))
    return zip_file_path

def send_email_notification(subject, body):
    """Send an email notification."""
    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    password = getpass.getpass("Enter your email password: ")

    message = f"""\
    Subject: {subject}

    {body}"""

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def backup_files(source_paths, target_dir, encryption_key=None):
    """Backup files and folders."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(target_dir, f"backup_{timestamp}")
    os.makedirs(backup_folder, exist_ok=True)

    for source_path in source_paths:
        if os.path.isfile(source_path):
            backup_file_path = os.path.join(backup_folder, os.path.basename(source_path))
            shutil.copy2(source_path, backup_file_path)
            logging.info(f"File backed up: {source_path}")
            if encryption_key:
                encrypt_file(backup_file_path, encryption_key)
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

    # Compress the backup folder
    zip_file_path = compress_backup(backup_folder)
    logging.info(f"Backup compressed: {zip_file_path}")

    # Send email notification
    send_email_notification("Backup Completed", f"Backup completed successfully. Backup file: {zip_file_path}")

def backup_database(db_path, target_dir, encryption_key=None):
    """Backup database file."""
    if os.path.isfile(db_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(target_dir, f"backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)
        db_backup_path = os.path.join(backup_folder, os.path.basename(db_path))
        shutil.copy2(db_path, db_backup_path)
        logging.info(f"Database backed up: {db_backup_path}")
        if encryption_key:
            encrypt_file(db_backup_path, encryption_key)
            logging.info(f"Database encrypted: {db_backup_path}")
        checksum = calculate_checksum(db_backup_path)
        logging.info(f"Checksum: {checksum}")
        print(f"Database backed up: {db_backup_path}")

        # Compress the backup folder
        zip_file_path = compress_backup(backup_folder)
        logging.info(f"Database backup compressed: {zip_file_path}")

        # Send email notification
        send_email_notification("Database Backup Completed", f"Database backup completed successfully. Backup file: {zip_file_path}")
    else:
        logging.warning(f"Database not found: {db_path}")
        print(f"Database not found: {db_path}")

if __name__ == "__main__":
    target_directory = "/path/to/backup/directory"
    encryption_password = getpass.getpass("Enter encryption password (optional): ")
    encryption_key = generate_key(encryption_password) if encryption_password else None

    print("Select what you want to back up:")
    print("1. Specific files")
    print("2. Specific folders")
    print("3. Database")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        files_to_backup = input("Enter the full paths of the files to back up (comma-separated): ")
        source_paths = [path.strip() for path in files_to_backup.split(',')]
        backup_files(source_paths, target_directory, encryption_key)
    elif choice == '2':
        folders_to_backup = input("Enter the full paths of the folders to back up (comma-separated): ")
        source_paths = [path.strip() for path in folders_to_backup.split(',')]
        backup_files(source_paths, target_directory, encryption_key)
    elif choice == '3':
        db_path = input("Enter the full path of the database file to back up: ")
        backup_database(db_path, target_directory, encryption_key)
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
