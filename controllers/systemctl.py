import subprocess as sub

from sys import platform
from shutil import copyfile

from interface import printing
from dataconstants import DRIVE_DEV_LOC

# Runs a command in the shell
def _run(command):
    try:
        process = sub.Popen(command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        return process.communicate()
    except Exception as e:
        printing.printf('Unknown exception on system._run(' + command + '):', end=' ', style=printing.ERROR,
                        log=True, logtag='system._run.error')
        printing.printf(e, style=printing.ERROR)


# Checks for a flash drive
def checkdev():
    return len(_run('ls ' + DRIVE_DEV_LOC)[0]) > 0

# Mounts a flash drive
def mount():
    if not checkdev():
        return None
    printing.printf('Found drive at ' + DRIVE_DEV_LOC + ', attempting to mount ...',
                    end=' ', style=printing.FLASH_DRIVE, log=True, logtag='system.mount')
    p = _run('udisksctl mount -b ' + DRIVE_DEV_LOC)
    error_string = p[1].decode('utf-8').strip('\n')
    if 'AlreadyMounted' in error_string:
        loc = error_string.split('mounted at')[1].strip(' .\'`')
        printing.printf("Drive already mounted to " + loc, style=printing.YELLOW,
                        log=True, logtag='system.mount')
        return loc
    elif error_string:
        printing.printf('Error mounting: ' + error_string, style=printing.ERROR,
                        log=True, logtag='system.mount.error')
        return None
    else:
        message = p[0].decode('utf-8').strip('\n')
        printing.printf(message, style=printing.FLASH_DRIVE,
                        log=True, logtag='system.mount')
        return message.split('at')[1].strip('. ')


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
    printing.printf('Unmounting drive from ' + DRIVE_DEV_LOC + ' ...', end=' ', style=printing.FLASH_DRIVE,
                    log=True, logtag='system.unmount')
    p = _run('udisksctl unmount -b ' + DRIVE_DEV_LOC)
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
            out = _run('system_profiler SPBluetoothDataType')
            return out[0].decode('utf8').split('\n')[5].split()[1]
        else:
            printing.printf('Server only runs on Linux & Mac, not Windows', style=printing.WARNING,
                            log=True, logtag='system.gethostMAC')
    except IndexError:
        if out[0]:
            printing.printf('No bluetooth adapter available', style=printing.ERROR,
                            log=True, logtag='system.gethostMAC.error')
        else:
            printing.printf('hcitool/system_profiler not found, please install it or edit systemctl.py to use something else',
                            style=printing.ERROR, log=True, logtag='system.gethostMAC.error')

