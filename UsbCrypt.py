
import os
from cryptography.fernet import Fernet
from PyQt5.QtCore import QObject, pyqtSignal

class UsbCrypt(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, mode, path, usbKeyName):
        super().__init__()
        self.keyDirectory = ".\keys\\"
        self.mode = mode
        self.path = path
        self.usbKeyName = usbKeyName
        
        self.filesCount = 0
        for root_dir, cur_dir, files in os.walk(path):
            self.filesCount += len(files)

    def run(self):
        if self.mode == True:
            self.encrypt()
        else:
            self.decrypt()
        self.finished.emit()

    def encrypt(self):
        generatedKey = self.createKey()
        self.saveKey(generatedKey, self.usbKeyName + ".key")
        loadedKey = self.loadKey(self.usbKeyName + ".key")

        self.encryptFile(loadedKey, self.path)

    def decrypt(self):
        loadedKey = self.loadKey(self.usbKeyName + ".key")
        self.decryptFile(loadedKey, self.path)

    def createKey(self):
        key = Fernet.generate_key()
        return key

    def saveKey(self, key, usbKeyName):
        with open(self.keyDirectory + usbKeyName, 'wb') as usbKey:
            usbKey.write(key)

    def loadKey(self, usbKeyName):
        with open(self.keyDirectory + usbKeyName, 'rb') as usbKey:
            key = usbKey.read()
        return key


    def encryptFile(self, key, path):
        f = Fernet(key)

        progressCounter = 0
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)

                with open(file_path, 'rb') as file:
                    original = file.read()

                encrypted = f.encrypt(original)

                progressCounter += 1
                self.progress.emit(str(round((progressCounter / self.filesCount) * 100)) + "%")

                with open (file_path, 'wb') as file:
                    file.write(encrypted)
        
        with open(path + "flag.crypt", 'w') as file:
            file.write("True")

        self.progress.emit("100%")
        


    def decryptFile(self, key, path):
        f = Fernet(key)

        try:
            os.remove(path + "flag.crypt")
        except:
            print("\n Unable to remove encryption flag: no flag is provided")

        progressCounter = 0
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)

                with open(file_path, 'rb') as file:
                    encrypted = file.read()

                decrypted = f.decrypt(encrypted)
                
                progressCounter += 1
                self.progress.emit(str(round((progressCounter / self.filesCount) * 100)) + "%")

                with open(file_path, 'wb') as file:
                    file.write(decrypted)

        self.progress.emit("100%")