from plyer import notification

def show_notification(title, message):
    """Display a notification with the provided title and message."""
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=10  # Notification duration (in seconds)
        )
        print(f"Notification sent: {title} - {message}")
    except Exception as e:
        print(f"Error sending notification: {e}")
