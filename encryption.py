'''User_input Password Data Protector'''
import base64

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
print('''
This Program should be used as a module.

This Program uses the cryptography module to lock the data with a String provided by a User.
For Added Security, It doesn't Stores the String anywhere in the file itself and rather converts 
The user input key into a base 64 encoded 32 byte key so that No other person can read the security code.
This program then encrypts the data with the key and stores the encrypted data with a random file extension which 
makes it hard for someone to accidently corrupt the encrypted key.

It also provides the functionality to decrypt the message upon asking for the key-string from the user.''')

SALT = b'\x92\x1a\xbf\x8c\x12\x8e\x45\x21\xab\xcd\xef\x12\x34\x56\x78\x90'

def validator(input_password):
    """returns the base64 url of a password"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=400_000,  # High iterations make brute-forcing incredibly hard
    )
    return base64.urlsafe_b64encode(kdf.derive(input_password.encode()))



def encrypt_file(file_path, password):
    key = validator(password)
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        text = file.read()

    encrypted_text = fernet.encrypt(text)

    with open(file_path,"wb") as file:
        file.write(encrypted_text)

def decrypt_file(file_path,password):
    key = validator(password)
    try:

        fernet = Fernet(key)

        with open(file_path, 'rb') as f:
            enc_text = f.read()
        dec_text = fernet.decrypt(enc_text)
        print("correct password")

       # with open(file_path, 'wb') as f:
        #    f.write(dec_text)
        return dec_text
    except InvalidToken:
        print("Incorrect Password")
        return 0


