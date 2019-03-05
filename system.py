import subprocess as sub

import printing
from dataconstants import MEDIA_DIR

DRIVE_DEV_LOCS = ['/dev/sdb', '/dev/sda', '/dev/sdc']


# Runs a command in the shell
def _run(command):
    process = sub.Popen(command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    return process.communicate()


# Checks for a flashdrive
def checkdev():
    devs = str(_run('ls /dev/sd*')[0])
    return [d for d in DRIVE_DEV_LOCS if devs.count(d) == 1]


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
        printing.printf('Mounting successful' + stdoutmessage(p[0]), style=printing.FLASH_DRIVE)
        return True


def copy(fin, fout):
    printing.printf('Copying ' + fin + ' to ' + fout + ' ...', end=' ', style=printing.FLASH_DRIVE)
    p = _run('sudo cp ' + fin + ' ' + fout)
    if p[1]:
        printing.printf('Error copying: ' + p[1].decode('utf-8'), style=printing.ERROR)
    else:
        printing.printf('Copying successful' + stdoutmessage(p[0]), style=printing.FLASH_DRIVE)


def unmount():
    printing.printf('Unmounting drive from ' + MEDIA_DIR + ' ...', end=' ', style=printing.FLASH_DRIVE)
    p = _run('sudo umount ' + MEDIA_DIR)
    if p[1]:
        printing.printf('Error unmounting: ' + p[1].decode('utf-8'), style=printing.ERROR)
    else:
        printing.printf('Unmounting successful, remove device' + stdoutmessage(p[0]), style=(printing.GREEN, printing.HIGHLIGHT))


# noinspection PyPep8Naming
def gethostMAC():
    try:
        return _run('hcitool dev')[0].decode('utf8').split('\n')[1].split()[1]
    except IndexError:
        printing.printf('No bluetooth adapter available', style=printing.ERROR)


def stdoutmessage(s):
    return ' with message: ' + s.decode('utf-8') if s else ''
