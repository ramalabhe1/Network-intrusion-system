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
        file_ready = wait_for_file_download(file_path)
        
        # If the file isn't ready, treat it as potentially unsafe
        if not file_ready:
            notify_file_status("File Detection", f"Detected file contains VIRUS or is CORRUPTED: '{os.path.basename(file_path)}'.")
            return
        
        # Check if the file is safe
        is_safe = check_file_safety(file_path)
        
        # Notify based on the file's safety status
        if is_safe:
            notify_file_status("File Safety Check", f"Detected file is SAFE: '{os.path.basename(file_path)}'.")
        else:
            notify_file_status("File Detection", f"Detected file contains VIRUS or is CORRUPTED: '{os.path.basename(file_path)}'.")

def wait_for_file_download(file_path):
    """Wait until the file is fully downloaded by monitoring its size stability."""
    stable_size_count = 0
    last_size = -1
    
    while stable_size_count < 2:  # Ensure file size is stable for 2 cycles
        try:
            current_size = os.path.getsize(file_path)
            if current_size == last_size:
                stable_size_count += 1
            else:
                stable_size_count = 0  # Reset if file size changes
            last_size = current_size
            time.sleep(0.5)
        except (FileNotFoundError, PermissionError):
            print(f"File not ready yet: {file_path}")
            # Notify immediately that the file is unsafe if it's not ready
            notify_file_status("File Detection", f"Detected file contains VIRUS or is CORRUPTED: '{os.path.basename(file_path)}'.")
            return False  # Mark file as not ready or unsafe
    print(f"File download completed: {file_path}")
    return True

def check_file_safety(file_path):
    """Check if the file is readable or corrupted."""
    try:
        # Try to open and read the file to ensure it is safe
        with open(file_path, 'rb') as file:
            file.read()
        print(f"File '{file_path}' is SAFE.")
        return True  # File is safe
    except Exception as e:
        print(f"File '{file_path}' is UNSAFE. Error: {e}")
        return False  # File is unsafe

def notify_file_status(title, message):
    """Send a notification using plyer."""
    print(f"Notification: {title} - {message}")
    notification.notify(
        title=title,
        message=message,
        timeout=5  # Display for 5 seconds
    )

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
