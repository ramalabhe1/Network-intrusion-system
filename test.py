from plyer import notification

# Simple notification test
notification.notify(
    title='Test Notification',
    message='This is a test notification!',
    timeout=10  # Notification duration (in seconds)
)
