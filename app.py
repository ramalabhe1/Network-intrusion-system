
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification

# Path to the Downloads folder
DOWNLOADS_FOLDER = "C:\\Users\\hp\\Downloads"

class DownloadEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Handle new file creation events in Downloads folder."""
        if event.is_directory:
            return  # Ignore directories
        file_path = event.src_path
        print(f"New file detected: {file_path}")
        
        # Wait for the file to be fully downloaded
        wait_for_file_download(file_path)
        
        # Check if the file is corrupted or contains any issue
        if check_file_safety(file_path):
            # If file is safe, show a notification saying it's safe
            notification.notify(
                title="File Detection",
                message=f"Detected file is safe: '{os.path.basename(file_path)}'.",
                timeout=5
            )
        else:
            # If file is not safe (corrupted or virus detected), show a notification for that
            notification.notify(
                title="File Detection",
                message=f"Detected file contains virus or is corrupted: '{os.path.basename(file_path)}'.",
                timeout=5
            )

def wait_for_file_download(file_path):
    """Wait until the file is fully downloaded by monitoring its size stability."""
    stable_size_count = 0
    last_size = -1
    
    while stable_size_count < 2:  # Check file size stability for 2 cycles
        try:
            current_size = os.path.getsize(file_path)
            print(f"Current file size: {current_size} bytes")
            
            if current_size == last_size:
                stable_size_count += 1
            else:
                stable_size_count = 0  # Reset if the size changes
            
            last_size = current_size
            time.sleep(0.5)
        except (FileNotFoundError, PermissionError):
            print(f"File not ready yet: {file_path}")
            time.sleep(0.5)
    
    print(f"File download completed: {file_path}")

def check_file_safety(file_path):
    """Attempt to read the file or handle any error to determine if it's corrupted."""
    try:
        # Try to open and read the file to check if it's safe
        with open(file_path, 'rb') as file:
            file.read()  # Try reading the file content
        print(f"File '{file_path}' is safe.")
        return True  # Return True if file is safe
    except Exception as e:
        # If the file cannot be read, it's likely corrupted or contains an issue
        print(f"File '{file_path}' appears to be corrupted or contains issues. Error: {e}")
        return False  # Return False if file is not safe

if __name__ == "__main__":
    # Set up the file system observer to monitor the Downloads folder
    event_handler = DownloadEventHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive=False)
    observer.start()

    print(f"Monitoring folder: {DOWNLOADS_FOLDER}")
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()  # Stop observing on exit
    observer.join()
