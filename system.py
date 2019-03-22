import subprocess as sub

import printing
from dataconstants import MEDIA_DIR

# Possible locations of a flash drive
DRIVE_DEV_LOCS = ['/dev/sdb', '/dev/sda', '/dev/sdc']


# Runs a command in the shell
def _run(command):
    process = sub.Popen(command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    return process.communicate()


# Checks for a flash drive
def checkdev():
    # Look through sd* devices, see if any of them are flash drives (but don't take the hard drive!)
    devs = str(_run('ls /dev/sd*')[0])
    return [d for d in DRIVE_DEV_LOCS if devs.count(d) == 1]


# Mounts a flash drive
def mount():
    devs = checkdev()
    if not devs:
        return False
    dev = devs[0]
    printing.printf('Found drive at ' + dev + ', attempting to mount to ' + MEDIA_DIR + ' ...',
                    end=' ', style=printing.FLASH_DRIVE)
    p = _run('sudo mount ' + dev + ' ' + MEDIA_DIR)
    if p[1]:
        printing.printf('Error mounting: ' + p[1].decode('utf-8'), style=printing.ERROR)
        return False
    else:
        printing.printf('Mounting successful' + _stdoutmessage(p[0]), style=printing.FLASH_DRIVE)
        return True


# Copies the data file to the mounted flash drive
def copy(fin, fout):
    printing.printf('Copying ' + fin + ' to ' + fout + ' ...', end=' ', style=printing.FLASH_DRIVE)
    p = _run('sudo cp ' + fin + ' ' + fout)
    if p[1]:
        printing.printf('Error copying: ' + p[1].decode('utf-8'), style=printing.ERROR)
    else:
        printing.printf('Copying successful' + _stdoutmessage(p[0]), style=printing.FLASH_DRIVE)


# Unmounts the flash drive
def unmount():
    printing.printf('Unmounting drive from ' + MEDIA_DIR + ' ...', end=' ', style=printing.FLASH_DRIVE)
    p = _run('sudo umount ' + MEDIA_DIR)
    if p[1]:
        printing.printf('Error unmounting: ' + p[1].decode('utf-8'), style=printing.ERROR)
    else:
        printing.printf('Unmounting successful, remove device' + _stdoutmessage(p[0]),
                        style=(printing.GREEN, printing.HIGHLIGHT))


# Finds the MAC address of the bluetooth adapter
# If hcitool is not installed, you can change the script to use some other command,
#   or you can just find it manually and hard code it in
# noinspection PyPep8Naming
def gethostMAC():
    out = ''
    try:
        out = _run('hcitool dev')
        return out[0].decode('utf8').split('\n')[1].split()[1]
    except IndexError:
        if out[0]:
            printing.printf('No bluetooth adapter available', style=printing.ERROR)
        else:
            printing.printf('hcitool not found, please install it or edit system.py to use something else',
                            style=printing.ERROR)


def _stdoutmessage(s):
    return ' with message: ' + s.decode('utf-8') if s else ''
