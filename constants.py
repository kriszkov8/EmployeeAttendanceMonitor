
HOST = "localhost"
DATABASE = "employeeattendacemonitor"
USER = "root"
PASSWORD = "qwerty123"

ENTRIES_DIR = r"C:\Users\Krisztian\Desktop\Tema\intrari"
BACKUP_ENTRIES_DIR = r"C:\Users\Krisztian\Desktop\Tema\backup_intrari"

DATE_FORMAT = "%Y-%M-%D"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = f"{DATE_FORMAT}T{TIME_FORMAT}.%fZ"

EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 587
EMAIL_USER = "your-email@example.com"
EMAIL_PASSWORD = "your-password"
MANAGER_EMAIL_TEMPLATE = "email_templates/manager_notification.txt"

MIN_WORKING_HOURS = 8