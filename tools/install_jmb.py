
import os, time
def get_dev():
    print("""
运行前提：
    1、手机开发者模式已打开，
    2、usb调试模式已打开，
    3、usb连接模式为文件传输
    4、个别手机需要授权usb进行引用安装
    5、个别手机可能会涉及传输完成后，手机点击安装
    """)
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