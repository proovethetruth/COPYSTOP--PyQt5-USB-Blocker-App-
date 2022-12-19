
import os
from cryptography.fernet import Fernet
from PyQt5.QtCore import QObject, pyqtSignal


class UsbCrypt(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, mode, path, usbName):
        super().__init__()
        self.keyDirectory = ".\keys\\"
        self.mode = mode
        self.path = path
        self.usbName = usbName

        self.filesCount = 0
        for root_dir, cur_dir, files in os.walk(path):
            self.filesCount += len(files)


    def run(self):
        if self.mode == True:
            self.encryptUsb()
        else:
            self.decryptUsb()
        return


    def encryptUsb(self):
        generatedKey = Fernet.generate_key()
        self.saveKey(generatedKey, self.usbName + ".key")
        self.encryptFile(generatedKey, self.path)


    def decryptUsb(self):
        key = self.getExistingKey(self.usbName + ".key")
        if key:
            self.decryptFile(key, self.path)
        else:
            print("\nNo such token")


    def getExistingKey(self, usbKeyName):
        try:
            with open(self.keyDirectory + usbKeyName, 'rb') as usbKey:
                key = usbKey.read()
                if key:
                    print("LOADED KEY " + str(key))
                    return key
        except:
            return None


    def saveKey(self, key, usbKeyName):
        print("SAVING KEY " + str(key))
        with open(self.keyDirectory + usbKeyName, 'wb') as usbKey:
            usbKey.write(key)


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
        self.finished.emit()
        


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

                if not (os.path.basename(file_path) == "WPsettings.dat" or os.path.basename(file_path) == "IndexerVolumeGuid"):
                    decrypted = f.decrypt(encrypted)
                
                progressCounter += 1
                self.progress.emit(str(round((progressCounter / self.filesCount) * 100)) + "%")

                os.remove(file_path)
                with open(file_path, 'wb') as file:
                    file.write(decrypted)
                file.close()

        self.progress.emit("100%")
        self.finished.emit()