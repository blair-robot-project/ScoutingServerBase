from queue import Queue
from threading import Thread
from shutil import get_terminal_size

from header import print_header
from dataconstants import DATA_FILE, MEDIA_DIR, HEADERS
from datafilectl import add_to_data_file, write_usb
from socketctl import connect, close

to_add = Queue()


def main():
    # Print instructions to fill width of screen
    width = get_terminal_size(fallback=(100, 24))[0]
    print_header(width)

    # Check if there is already a data file, if not, make one
    try:
        f = open(DATA_FILE, 'r')
        d = f.read()
        f.close()
        if not d:
            raise FileNotFoundError
    except FileNotFoundError:
        f = open(DATA_FILE, 'w')
        f.write(HEADERS + '\n')
        f.close()

    print('Waiting for connections')

    Thread(target=connect).start()

    while True:
        try:
            # If there is data to add, add it to the file
            if not to_add.empty():
                add_to_data_file(to_add.get())
            # elif listdir(MEDIA_DIR):
            #     write_usb()
        except KeyboardInterrupt:
            q = input('Are you sure you want to quit? (y/n) ')
            if q == 'y':
                # Finish adding data
                while not to_add.empty():
                    add_to_data_file(to_add.get())
                close()
                break


if __name__ == '__main__':
    main()
