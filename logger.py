from time import strftime

from dataconstants import LOG_FILE


def log(tag, msg):
    f = open(LOG_FILE, 'a')
    f.write('{tag:20s}: [{time:s}] {msg:s}\n'.format(tag=tag, time=strftime('%d.%m.%y %H;%M;%S'),
                                                     msg=msg.replace(':', ';')))
