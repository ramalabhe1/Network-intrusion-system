import zipfile
import pyclamd
from alert import show_notification  # Import show_notification from alert.py

def is_zip_corrupted(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.testzip()  # Check the integrity of the zip file
        return False  # ZIP file is not corrupted
    except (zipfile.BadZipFile, zipfile.LargeZipFile, FileNotFoundError):
        return True  # ZIP file is corrupted

def is_file_infected(file_path):
    cd = pyclamd.ClamdUnixSocket()  # Adjust if needed (or use ClamdNetworkSocket)
    try:
        result = cd.scan_file(file_path)  # Scan the file for viruses
        if result is None:
            return False  # File is clean
        else:
            return True  # File contains a virus
    except pyclamd.ClamdError as e:
        print(f"ClamAV error: {e}")
        return False  # If error occurs, assume clean

def scan_file(file_path):
    if is_zip_corrupted(file_path):
        show_notification("The file is corrupted!")
    elif is_file_infected(file_path):
        show_notification("The file contains a virus!")
    else:
        show_notification("The file is clean and not corrupted.")
