import base64


def base64_decoder(txt: str):
    try:
        decoded_bytes = base64.b64decode(txt)
        # Convert the bytes to a string
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        raise Exception(f"Error while decoding base64 encoded txt: {e}")

