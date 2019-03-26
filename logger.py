from time import strftime

from dataconstants import LOG_FILE


def log(tag, msg):
    f = open(LOG_FILE, 'a')
    f.write('{tag:22s}: [{time:s}] {msg:s}\n'.format(tag=tag, time=strftime('%d.%m.%y %H;%M;%S'), msg=_clean(msg)))
    f.close()


def _clean(s):
    return s.replace('\n', '\\n').replace('\t', '\\t').replace(':', ';')
