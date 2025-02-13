import os
import shutil
import datetime

def backup_files(source_paths, target_dir):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(target_dir, f"backup_{timestamp}")

    os.makedirs(backup_folder, exist_ok=True)

    for source_path in source_paths:
        if os.path.isfile(source_path):
            shutil.copy2(source_path, backup_folder)
            print(f"File backed up: {source_path}")
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, os.path.join(backup_folder, os.path.basename(source_path)))
            print(f"Folder backed up: {source_path}")
        else:
            print(f"Skipped: {source_path} (not a file or folder)")

def backup_database(db_path, target_dir):
    if os.path.isfile(db_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(target_dir, f"backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)
        db_backup_path = os.path.join(backup_folder, os.path.basename(db_path))
        shutil.copy2(db_path, db_backup_path)
        print(f"Database backed up: {db_backup_path}")
    else:
        print(f"Database not found: {db_path}")

if __name__ == "__main__":
    target_directory = "/path/to/backup/directory"  # Change this to your target directory

    print("Select what you want to back up:")
    print("1. Specific files")
    print("2. Specific folders")
    print("3. Database")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        files_to_backup = input("Enter the full paths of the files to back up (comma-separated): ")
        source_paths = [path.strip() for path in files_to_backup.split(',')]
        backup_files(source_paths, target_directory)

    elif choice == '2':
        folders_to_backup = input("Enter the full paths of the folders to back up (comma-separated): ")
        source_paths = [path.strip() for path in folders_to_backup.split(',')]
        backup_files(source_paths, target_directory)

    elif choice == '3':
        db_path = input("Enter the full path of the database file to back up: ")
        backup_database(db_path, target_directory)

    else:
        print("Invalid choice. Please select 1, 2, or 3.")
