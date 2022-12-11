
from UsbWidget import *

import wmi, pythoncom
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
            try:
                insertedUsb = insertionWatcher(timeout_ms = 10)
            except wmi.x_wmi_timed_out:
                pass
            else:
                if insertedUsb:
                    insertedUsbName = insertedUsb.VolumeName + " (" + insertedUsb.name + ")"
                    self.receivedName.emit(insertedUsbName)

            try:
                removedUsb = removalWatcher(timeout_ms = 10)
            except wmi.x_wmi_timed_out:
                pass
            else:
                if removedUsb:
                    removedUsbName = removedUsb.VolumeName + " (" + removedUsb.name + ")"
                    self.removedName.emit(removedUsbName)