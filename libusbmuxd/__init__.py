"""Python bindings for libusbmuxd"""

__version__ = '0.1'

import ctypes
from typing import Optional, List

LIBUSBMUXD = ctypes.cdll.LoadLibrary("libusbmuxd-2.0.dylib")

DEVICE_LOOKUP_USBMUX = 1
DEVICE_LOOKUP_NETWORK = 2
DEVICE_LOOKUP_PREFER_NETWORK = 4

CONNECTION_TYPE_USB = 1
CONNECTION_TYPE_NETWORK = 2

UE_DEVICE_ADD = 1
UE_DEVICE_REMOVE = 2
UE_DEVICE_PAIRED = 3


class _DeviceInfo(ctypes.Structure):
    _fields_ = [('handle', ctypes.c_uint32),
                ('product_id', ctypes.c_uint32),
                ('udid', ctypes.c_char * 44),
                ('conn_type', ctypes.c_uint32),
                ('conn_data', ctypes.c_char * 200)]


class MuxDevice:
    def __init__(self, device_info):
        self.device_info = device_info

    @staticmethod
    def list():
        devices: List['MuxDevice'] = []
        api_list = ctypes.c_void_p()
        device_count = LIBUSBMUXD.usbmuxd_get_device_list(ctypes.pointer(api_list))
        if device_count > 0:
            ctypes.cast(api_list, device_count * ctypes.POINTER(_DeviceInfo))
        LIBUSBMUXD.usbmuxd_device_list_free(ctypes.pointer(api_list))
        return devices

    @staticmethod
    def get(udid: str) -> Optional['MuxDevice']:
        result = _DeviceInfo()
        status = LIBUSBMUXD.usbmuxd_get_device_by_udid(udid, ctypes.POINTER(result))

        if status == 1:
            return MuxDevice(result)

        return None


class MuxConnection:
    def __init__(self, device, port):
        self.device = device
        self.port = port

    def connect(self):
        pass
