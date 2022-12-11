
from UsbWidget import *

from cryptography.fernet import Fernet
import wmi, time, pythoncom
from PyQt5.QtCore import QObject, pyqtSignal

class UsbCrypt():
    progress = pyqtSignal(int)

    def __init__(self, path,):
        super().__init__()

        self.keyDirectory = "keys/"

        # mykey = self.key_create()
        # self.key_write(mykey, 'keys/public.key')
        # loaded_key = self.key_load('keys/public.key')

        self.file_encrypt(loaded_key, path, path)
        self.file_decrypt(loaded_key, path, path)

    def encrypt(self, path, UsbName):
        generatedKey = self.key_create()
        self.key_write(generatedKey, self.keyDirectory + UsbName + ".key")
        loaded_key = self.key_load(self.keyDirectory + UsbName + ".key")

        self.file_encrypt(loaded_key, path, path)

    def key_create(self):
        key = Fernet.generate_key()
        return key

    def key_write(self, key, key_name):
        with open(key_name, 'wb') as mykey:
            mykey.write(key)

    def key_load(self, key_name):
        with open(key_name, 'rb') as mykey:
            key = mykey.read()
        return key


    def file_encrypt(self, key, original_file, encrypted_file):
        f = Fernet(key)

        with open(original_file, 'rb') as file:
            original = file.read()

        encrypted = f.encrypt(original)

        with open (encrypted_file, 'wb') as file:
            file.write(encrypted)


    def file_decrypt(self, key, encrypted_file, decrypted_file):
        f = Fernet(key)

        with open(encrypted_file, 'rb') as file:
            encrypted = file.read()

        print(encrypted)
        decrypted = f.decrypt(encrypted)

        with open(decrypted_file, 'wb') as file:
            file.write(decrypted)

# class EncryptionWorker(QObject):
#     def __init__(self, key):
#         super().__init__()

#     def run():
#         f = Fernet(key)

#         with open(original_file, 'rb') as file:
#             original = file.read()

#         encrypted = f.encrypt(original)

#         with open (encrypted_file, 'wb') as file:
#             file.write(encrypted)