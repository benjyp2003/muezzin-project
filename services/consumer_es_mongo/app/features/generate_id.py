import hashlib


def generate_unique_id(size, file_name):
    """Generates a unique ID based on a hash on the file size and the file name"""
    try:
        data_string = str(size) + file_name

        # Using SHA-256
        sha256_hash = hashlib.sha256(data_string.encode('utf-8')).hexdigest()[:15]
        return sha256_hash

    except Exception as e:
        raise Exception(f"An error accord while generating a unique ID: {e}")


