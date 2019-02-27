import subprocess as sub

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
    print('Found drive at ' + dev + ', attempting to mount to ' + MEDIA_DIR + ' ...', end=' ')
    p = _run('sudo mount ' + dev + ' ' + MEDIA_DIR)
    if p[1]:
        print('Error mounting: ' + p[1].decode('utf-8'))
        return False
    else:
        print('Mounting successful' + stdoutmessage(p[0]))
        return True


def copy(fin, fout):
    print('Copying ' + fin + ' to ' + fout + ' ...', end=' ')
    p = _run('sudo cp ' + fin + ' ' + fout)
    if p[1]:
        print('Error copying: ' + p[1].decode('utf-8'))
    else:
        print('Copying successful' + stdoutmessage(p[0]))


def unmount():
    print('Unmounting drive from ' + MEDIA_DIR + ' ...', end=' ')
    p = _run('sudo umount ' + MEDIA_DIR)
    if p[1]:
        print('Error unmounting: ' + p[1].decode('utf-8'))
    else:
        print('Unmounting successful' + stdoutmessage(p[0]))


def stdoutmessage(s):
    return ' with message: ' + s.decode('utf-8') if s else ''
