from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


def write_log(message):
    with open(f"{os.getenv('LOGS_PATH')}", "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')} - {message}\n")
