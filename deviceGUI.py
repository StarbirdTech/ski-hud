import tkinter as tk
import serial.tools.list_ports
import platform

if platform.system() == 'Windows':
    import win32api
    import win32con
    import win32gui
elif platform.system() == 'Darwin':
    import objc
else:
    import pyudev


class SerialDeviceGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Serial Devices")
        self.devices_listbox = tk.Listbox(self.master)
        self.devices_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.refresh_button = tk.Button(self.master, text="Refresh", command=self.refresh_devices)
        self.refresh_button.pack(pady=10)

        # Attach event listeners for device connect and disconnect
        if platform.system() == 'Windows':
            self.WM_DEVICECHANGE = 0x0219
            self.DEVICE_ARRIVAL = 0x8000
            self.DEVICE_REMOVAL = 0x8004
            self.hwnd = self.master.winfo_id()
            self.WndProc = win32con.WNDPROC(self.handle_device_event)
            win32gui.SetWindowLong(self.hwnd, win32con.GWL_WNDPROC, self.WndProc)
        elif platform.system() == 'Darwin':
            self.IOServiceMatching = objc.lookUpClass('IOServiceMatching')
            self.kIOMasterPortDefault = 0
            self.kIOFirstMatchNotification = 1
            self.kIOTerminatedNotification = 2
            self.callback = objc.selector(self.handle_device_event, signature='v@:@')
            self.match_dict = {'IOProviderClass': 'IOUSBDevice'}
            self.notify_object = None
            self.runLoop = objc.lookUpClass('NSRunLoop').currentRunLoop()
        else:
            self.context = pyudev.Context()
            self.monitor = pyudev.Monitor.from_netlink(self.context)
            self.monitor.filter_by(subsystem='tty')
            self.monitor_observer = self.context.monitor_observer(self.handle_device_event)
            self.monitor_observer.start()

        self.refresh_devices()

    def handle_device_event(self, hwnd, msg, wparam, lparam):
        if msg == self.WM_DEVICECHANGE and (wparam == self.DEVICE_ARRIVAL or wparam == self.DEVICE_REMOVAL):
            self.refresh_devices()
        else:
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def handle_device_added(self, refcon, iterator):
        self.refresh_devices()

    def handle_device_removed(self, refcon, iterator):
        self.refresh_devices()

    def refresh_devices(self):
        self.devices_listbox.delete(0, tk.END)
        devices = serial.tools.list_ports.comports()
        if not devices:
            self.devices_listbox.insert(tk.END, "No devices connected")
            self.master.geometry("300x100")
        else:
            for device in devices:
                self.devices_listbox.insert(tk.END, f"{device.device} - {device.description}")
            device_count = len(devices)
            self.master.geometry(f"300x{device_count * 25 + 100}")


if __name__ == '__main__':
    root = tk.Tk()
    gui = SerialDeviceGUI(root)
    root.mainloop()
