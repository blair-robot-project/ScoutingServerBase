from os import listdir
from subprocess import run

from dataconstants import DATA_FILE


# Adds a match to the data file
def add_to_data_file(match):
    f = open(DATA_FILE, 'r')
    s = f.read()
    f.close()
    f = open(DATA_FILE, 'w')
    s += match[1] + '\n'
    f.write(s)
    f.close()


# Writes data to a removable device
def write_usb():
    ...

# 	ls = listdir(MEDIA_DIR)
# 	if ls:
# 		dataf = open(DATA_FILE)
# 		data = dataf.read()
# 		dataf.close()
# 		usb = open(MEDIA_DIR+'/'+ls[0]+'/'+DATA_FILE,'w')
# 		usb.write(data)
# 		usb.close()
