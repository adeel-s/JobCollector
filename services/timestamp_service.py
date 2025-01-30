from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re

def getTimestamp(text):
    """Convert a relative job posting time (e.g., '1 month ago') into an SQL timestamp."""
    # Define the current timestamp
    now = datetime.now()
    
    # Extract the numeric value and time unit using regex
    match = re.search(r"(\d+)\s*(hour|day|week|month|year)s?\s*ago", text, re.IGNORECASE)
    
    if not match:
        return None  # Return None if the text format is not recognized
    
    num = int(match.group(1))  # Extract the number (e.g., 1, 2, 3)
    unit = match.group(2).lower()  # Extract the time unit (e.g., day, week)
    
    # Adjust the current time based on the extracted values
    if unit == "hour":
        job_date = now
    elif unit == "day":
        job_date = now - timedelta(days=num)
    elif unit == "week":
        job_date = now - timedelta(weeks=num)
    elif unit == "month":
        job_date = now - relativedelta(months=num)
    elif unit == "year":
        job_date = now - relativedelta(years=num)
    else:
        return None  # Handle unexpected cases

    # Format as SQL timestamp
    return job_date.strftime("%Y-%m-%d %H:%M:%S")

def getReleative(timestamp):
    """Convert an SQL timestamp to a human-readable 'time ago' format."""
    now = datetime.now()
    job_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    delta = now - job_date

    # Convert to human-friendly format
    if delta < timedelta(seconds=60):
        return "just now"
    elif delta < timedelta(minutes=60):
        minutes = delta.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif delta < timedelta(hours=24):
        hours = delta.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif delta < timedelta(days=7):
        days = delta.days
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif delta < timedelta(days=30):
        weeks = delta.days // 7
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    elif delta < timedelta(days=365):
        months = relativedelta(now, job_date).months
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = relativedelta(now, job_date).years
        return f"{years} year{'s' if years > 1 else ''} ago"
