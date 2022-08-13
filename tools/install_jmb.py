
import os, time
def get_dev():
    rt = os.popen('adb devices').readlines()
    rt = rt[1:-1]
    for i in rt:
        dev = i.split('\t')
        uni = "adb -s {} uninstall com.jmbon.android".format(dev[0])
        os.popen(uni)
        time.sleep(1)
        inst = r"adb -s {} install E:\jmbon\apk\debug\app-debug.apk".format(dev[0])
        os.popen(inst)

if __name__ == '__main__':
    get_dev()