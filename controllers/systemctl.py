import os
import subprocess as sub

from sys import platform
from shutil import copyfile
from time import sleep

from interface import printing

# Runs a command in the shell
def _run(command):
    try:
        process = sub.Popen(command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        return process.communicate()
    except Exception as e:
        printing.printf('Unknown exception on system._run(' + command + '):', end=' ', style=printing.ERROR,
                        log=True, logtag='system._run.error')
        printing.printf(e, style=printing.ERROR)


# From https://askubuntu.com/questions/938255/how-to-perform-the-same-operation-as-pressing-the-eject-button-in-nautilus-by-r
def find_usb_partitions():
    parts = tuple(
        os.path.realpath(os.path.join('/dev/disk/by-id', p))
        for p in os.listdir('/dev/disk/by-id')
        if p.startswith('usb-')
    )
    parts_numbered = set()
    for p in parts:
        p_strip = p.rstrip('0123456789')
        if p != p_strip:
            parts_numbered.add(p_strip)
    parts = tuple(p for p in parts if p not in parts_numbered)
    del parts_numbered
    return parts

def find_mounted_usbs():
    devs = []
    with open('/proc/mounts') as mounts:
        for line in mounts:
            if line.startswith('/dev/'):
                devs.append(line.split(' ', 1)[0])
    return [d for d in devs if d in find_usb_partitions()]


# Checks for a flash drive
def checkdev():
    return len(find_usb_partitions()) > 0


def get_mount_point(block):
    p = _run('udiskctl info -b ' + block)
    if p[1]:
        return None
    else:
        return [l for l in p[0].decode('utf-8').split('\n') if 'MountPoints:' in l].split(':')[1].split(',')[0].strip()


# Mounts a flash drive
def mount():
    devs = find_usb_partitions()
    if not devs: return None
    dev = [d for d in devs if d not in find_mounted_usbs()]
    if not dev: 
        loc = get_mount_point(devs[0])
        printing.printf('Drive ' + devs[0] + ' already mounted to ' + loc, style=printing.YELLOW,
                            log=True, logtag='system.mount')
        return loc
    done = 0
    printing.printf('Found drive at ' + dev[0] + ', attempting to mount ...', end=' ', style=printing.FLASH_DRIVE)
    while done < 10:
        p = _run('udisksctl mount -b ' + dev[0])
        error_string = p[1].decode('utf-8').strip('\n')
        if 'Error looking up object for device' in error_string:
            sleep(.2)
            done += 1
        elif error_string:
            printing.printf('Error mounting: ' + error_string, style=printing.ERROR,
                            log=True, logtag='system.mount.error')
            return None
        else:
            message = p[0].decode('utf-8').strip('\n')
            printing.printf(message, style=printing.FLASH_DRIVE,
                            log=True, logtag='system.mount')
            return message.split('at')[1].strip('. ')
    printing.printf('Error mounting: ' + error_string, style=printing.ERROR,
                            log=True, logtag='system.mount.error')
    return None


# Copies the data file to the mounted flash drive
def copy(fin, fout):
    printing.printf('Copying ' + fin + ' to ' + fout + ' ...', end=' ', style=printing.FLASH_DRIVE,
                    log=True, logtag='system.copy')
    
    # with open(fout, 'w') as f:
        # f.write(open(fin).read())
    #copyfile(fin, fout)
    p = _run('cp ' + fin + ' ' + fout)
    if p[1]:
       printing.printf('Error copying: ' + p[1].decode('utf-8'), style=printing.ERROR,
                       log=True, logtag='system.copy.error')
    else:
       printing.printf('Copying successful', style=printing.FLASH_DRIVE,
                       log=True, logtag='system.copy')


# Unmounts the flash drive
def unmount():
    for dev in find_mounted_usbs():
        printing.printf('Unmounting drive from ' + dev + ' ...', end=' ', style=printing.FLASH_DRIVE,
                        log=True, logtag='system.unmount')
        p = _run('udisksctl unmount -b ' + dev)
        if p[1]:
            printing.printf('Error unmounting: ' + p[1].decode('utf-8'), style=printing.ERROR,
                            log=True, logtag='system.unmount.error')
        else:
            printing.printf('Unmounting successful, remove device',
                            style=printing.FLASH_DRIVE_SUCCESS, log=True, logtag='system.unmount')


# Finds the MAC address of the bluetooth adapter
# If hcitool is not installed, you can change the script to use some other command,
#   or you can just find it manually and hard code it in
def gethostMAC():
    out = ''
    try:
        if platform == 'linux':
            out = _run('hcitool dev')
            return out[0].decode('utf8').split('\n')[1].split()[1]
        elif platform == 'darwin': #macOS
            # Mac is not yet fully supported
            out = _run('system_profiler SPBluetoothDataType')
            return out[0].decode('utf8').split('\n')[5].split()[1]
        else:
            printing.printf('Server only runs on Linux, not Windows', style=printing.WARNING,
                            log=True, logtag='system.gethostMAC')
    except IndexError:
        if out[0]:
            printing.printf('No bluetooth adapter available', style=printing.ERROR,
                            log=True, logtag='system.gethostMAC.error')
        else:
            printing.printf('hcitool/system_profiler not found, please install it or edit systemctl.py to use something else',
                            style=printing.ERROR, log=True, logtag='system.gethostMAC.error')

