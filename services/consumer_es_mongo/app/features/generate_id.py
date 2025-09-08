import random

def generate_unique_id(size):
    """Generates a unique ID based on the file size and a random number"""
    try:
        random_number = random.SystemRandom().randint(0, 9999)

        # Combine the size and random component into a string
        unique_id = f"{size}-{random_number}"
        return unique_id

    except Exception as e:
        raise Exception(f"An error accord while generating a unique ID: {e}")
