import zipfile
import pyclamd
from plyer import notification

# Function to check if a ZIP file is corrupted
def is_zip_corrupted(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.testzip()
        return False  # ZIP file is not corrupted
    except (zipfile.BadZipFile, zipfile.LargeZipFile, FileNotFoundError):
        return True  # ZIP file is corrupted or unreadable

# Function to check if a file is infected with a virus using ClamAV
def is_file_infected(file_path):
    cd = pyclamd.ClamdUnixSocket()
    try:
        result = cd.scan_file(file_path)
        if result is None:
            return False  # File is clean
        else:
            return True  # File contains a virus
    except pyclamd.ClamdError as e:
        print(f"ClamAV error: {e}")
        return False  # Assume file is clean in case of ClamAV error

# Function to show desktop notifications
def show_notification(message):
    notification.notify(
        title="File Integrity and Virus Check",
        message=message,
        timeout=10  # Notification for 10 seconds
    )

# Main function
def check_file(file_path):
    if is_zip_corrupted(file_path):
        show_notification("The ZIP file is corrupted!")
    elif is_file_infected(file_path):
        show_notification("The file contains a virus!")
    else:
        show_notification("The file is not corrupted and is clean.")
        
# Example usage
file_path = "path_to_your_file.zip"  # Replace with the path to your ZIP file
check_file(file_path)
