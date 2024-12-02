# generate_key.py
from cryptography.fernet import Fernet

def generate_key():
    """
    Generates a key and saves it into a file named 'secret.key'.
    """
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    print("Encryption key generated and saved to 'secret.key'.")

if __name__ == '__main__':
    generate_key()
