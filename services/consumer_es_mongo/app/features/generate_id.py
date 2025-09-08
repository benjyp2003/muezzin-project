import random
from datetime import datetime

def generate_unique_id_with_timestamp(timestamp='1979-12-31 23:00:00.000'):
    try:
        date_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        # Generate a random number to ensure uniqueness within the same millisecond
        random_number = random.SystemRandom().randint(0, 99999)

        # Combine the timestamp and random component into a string
        unique_id = f"{date_object}-{random_number}"
        return unique_id

    except Exception as e:
        raise Exception(f"An error accord while generating a unique ID: {e}")
