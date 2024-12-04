# generate_key.py
from cryptography.fernet import Fernet

"""
- Generates a key and saves it into a file named secret.key for accessing data from hdisres.json file.
"""
    
if __name__ == '__main__':
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
