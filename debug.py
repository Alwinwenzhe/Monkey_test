import os, time

class Debug(object):

    app_name = "com.jmbon.android"
    path = os.path.abspath(os.path.dirname(__file__)) + r'\bugreport_out'

    def GetDeviceAndPackage(self):
        """获取当前连接的设备信息"""
        # 具有清屏功能
        os.system("cls")
        # 执行系统命令并返回执行后的结果
        rt = os.popen('adb devices').readlines()

        n = len(rt) - 2
        print("当前已连接待测手机数为：" + str(n))

        print("monkey测试即将开始......")
        self.count = input("请输入你要进行的monkey测试次数：")
        self.testmodel = input("请输入你是要进行单次测试还是多次连续测试，请输入（1-代表单次测试，2-代表多次连续测试）：")
        ds = []
        for i in range(n):
            nPos = rt[i + 1].index("\t")
            ds.append(rt[i + 1][:nPos])
            self.dev = ds[i]
            # 获取系统版本
            cmd_s = 'adb -s {} shell getprop ro.build.version.release'.format(self.dev)
            release = os.popen(cmd_s).readline().replace('\n', '')
            # 获取手机型号
            cmd_s = 'adb -s {} shell getprop ro.product.model'.format(self.dev)
            self.model = os.popen(cmd_s).readline().replace('\n', '')
            # 手机厂商
            cmd_s = 'adb -s {} shell getprop ro.product.brand'.format(self.dev)
            brand = os.popen(cmd_s).readline().replace('\n', '')

            # 查找测试的app
            cmd_s = 'adb -s {}  shell pm list packages | find "{}"'.format(self.dev, self.app_name)
            self.packagename = os.popen(cmd_s).readline().replace('\n', '')
            if self.packagename is None:
                # 手机未安装
                print(' {} is not installed in {}.'.format(self.app_name, self.model))
                break
            else:
                self.packagename = self.packagename.split(':')[-1]

    def CreateMonkeyFile(self):
        """生成monkey脚本"""
        # 测试记录存放位置
        self.GetDeviceAndPackage()
        filedir = os.path.exists(self.path)
        if filedir:
            # print ("File Exist!")
            pass
        else:
            os.mkdir(self.path)

        self.path_app = self.path + '\\' + self.app_name
        filedir = os.path.exists(self.path_app)
        if filedir:
            # print("File Exist!")
            pass
        else:
            os.mkdir(self.path_app)

        # 按设备ID生成日志目录文件夹
        path_device = self.path_app + '\\' + self.app_name + '-' + self.model
        devicedir = os.path.exists(path_device)

        if devicedir:
            # print ("File exist!")
            pass
        else:
            os.mkdir(path_device)

        file_cmd = self.path_app + '\\' + self.model + '-logcat' + '.cmd'
        wl = open(file_cmd, 'w')

        wl.write(
            'adb -s ' + self.dev + ' logcat -v time *:W > ' + path_device + '\\logcat_%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%.txt\n')
        wl.close()

        # monkey脚本文件
        file_cmd = self.path_app + '\\' + self.model + '.cmd'
        # 通用monkey命令
        # 指定系统事件百分比
        syskeys = 5
        # 调整触摸事件的百分比
        touch = 55
        # 调整动作事件的百分比
        motion = 20
        # 指定Activity启动的百分比
        appswitch = 0
        # 指定其他事件的百分比
        anyevent = 20
        # 在事件之间插入特定的延时时间
        throttle = 300
        cmd_s = 'adb -s {} shell monkey -p {} --monitor-native-crashes --ignore-crashes --pct-syskeys {} --pct-touch {} --pct-appswitch {} --pct-anyevent {} --pct-motion {} --throttle {} -s %random% -v {} > {}\\monkey_%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%.txt\n'.format(
            self.dev, self.packagename, syskeys, touch, motion, appswitch, anyevent, throttle, self.count, path_device)
        if self.testmodel == '1':
            wd = open(file_cmd, 'w')
            wd.write(cmd_s)
            wd.write('@echo 测试成功完成，请查看日志文件~')
            wd.close()
        elif self.testmodel == '2':
            wd = open(file_cmd, 'w')
            wd.write(':loop')
            wd.write('set num = 1')
            wd.write('\nset /a num+=1')
            wd.write('\nif "%num%"=="4" goto end')
            wd.write('\n' + cmd_s)
            wd.write('@echo 测试成功完成，请查看日志文件~')
            wd.write('\nadb -s ' + self.dev + ' shell am force-stop ' + self.app_name)
            wd.write('\n@ping -n 15 127.0.0.1 >nul')
            wd.write('\ngoto loop')
            wd.write('\n:end')
            wd.close()

    def RunMonkey(self):
        self.CreateMonkeyFile()
        for file in os.listdir(self.path_app):
            if os.path.isfile(os.path.join(self.path_app, file)) == True:
                if file.find('.cmd') > 0:
                    os.system('start ' + os.path.join(self.path_app, '"' + file + '"'))  # dos命令中文件名如果有空格，需加上双引号
                    time.sleep(1)


if __name__ == '__main__':
    d = Debug()
    d.RunMonkey()


