from datetime import datetime

def timestamp_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

