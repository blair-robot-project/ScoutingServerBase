from threading import Thread

from controllers import systemctl


class DriveController:
    def __init__(self):
        self.data_changed = True
        self.watching = False
        self.device = ''
        self.mount_point = ''
    
    def start_monitoring(self):
        Thread(target=self.monitor).start()

    def monitor(self):
        for line in systemctl.continued_execute(['udisksctl','monitor']):
            if self.watching:
                if 'ConnectionBus' in line and 'usb' not in line:
                    self.watching = False
                elif 'Device' in line:
                    self.device = extract_value(line)
                elif 'fat' in line.casefold():
                    
            elif 'ConnectionBus' in line and 'usb' in line:
                self.watching = True


def extract_value(line):
    return line.split(':')[1].strip() if ':' in line else ''
