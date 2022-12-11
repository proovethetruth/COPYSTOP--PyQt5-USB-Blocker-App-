
from UsbWidget import *

import wmi, time, pythoncom
from PyQt5.QtCore import QObject, pyqtSignal

class UsbListener(QObject):
    receivedName = pyqtSignal(str)
    removedName = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        pythoncom.CoInitialize()
        c = wmi.WMI ()

        insertionQuery = "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_LogicalDisk\'"
        removalQuery = "SELECT * FROM __InstanceDeletionEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_LogicalDisk\'"

        insertionWatcher = c.watch_for(raw_wql = insertionQuery)
        removalWatcher = c.watch_for(raw_wql = removalQuery)
        while True:
            insertedUsb = insertionWatcher()
            insertedUsbName = insertedUsb.VolumeName + " (" + insertedUsb.name + ")"
            self.receivedName.emit(insertedUsbName)

            removedUsb = removalWatcher()
            removedUsbName = removedUsb.VolumeName + " (" + insertedUsb.name + ")"
            self.removedName.emit(removedUsbName)

            time.sleep(3)