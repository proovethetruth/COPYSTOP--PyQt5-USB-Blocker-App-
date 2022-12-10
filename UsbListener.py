
from UsbWidget import *

import wmi, time, pythoncom
from PyQt5.QtCore import QObject, QThread, pyqtSignal

class UsbListener(QObject):
    receivedName = pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def run(self):
        pythoncom.CoInitialize()
        raw_wql = "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_LogicalDisk\'"
        c = wmi.WMI ()
        watcher = c.watch_for(raw_wql = raw_wql)
        while True:
            usb = watcher()
            usbFullName = usb.VolumeName + " (" + usb.name + ")"
            self.receivedName.emit(usbFullName)
            time.sleep(3)