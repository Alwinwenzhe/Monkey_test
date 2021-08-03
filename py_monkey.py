# STATUS: PASS
# Time: 2021-08-02

import os, time
import datetime

class PyMonkey():

    def __init__(self,*args,**kwargs):
        self.app_name = "com.jmbon.android"
        self.path = os.path.abspath(os.path.dirname(__file__)) + r'\bugreport_out'

    def run_time(self,end,start,*args,**kwargs):
        '''
        运行时长
        :param end:
        :param start:
        :return:
        '''
        runtime = int( end - start)
        return runtime

    def GetDeviceAndPackage(self,*args,**kwargs):
        """获取当前连接的设备信息"""
        # 具有清屏功能
        self.start_time = time.time()
        os.system("cls")
        # 执行系统命令并返回执行后的结果
        rt = os.popen('adb devices').readlines()

        n = len(rt) - 2
        print("当前已连接待测手机数为：" + str(n))

        print("monkey测试即将开始......\n Monkey单次运行的事件数默认为20000")
        # self.count = input("请输入Monkey单次运行时，事件数：")
        self.testmodel = input("请输入Monkey循环运行次数：")
        self.ds = []
        self.model_list = []
        for i in range(n):
            nPos = rt[i + 1].index("\t")            # 通过index获得设备ID长度
            self.ds.append(rt[i + 1][:nPos])
            self.dev = self.ds[i]
            # 获取系统版本
            cmd_s = 'adb -s {} shell getprop ro.build.version.release'.format(self.dev)
            release = os.popen(cmd_s).readline().replace('\n', '')
            # 获取手机型号
            cmd_s = 'adb -s {} shell getprop ro.product.model'.format(self.dev)
            self.model = os.popen(cmd_s).readline().replace('\n', '')
            self.model_list.append(self.model)
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


    def CreateMonkeyFile(self,*args,**kwargs):
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

            ds_i = 0
            for i in self.model_list:
                # 按设备ID生成日志目录文件夹
                path_device = self.path_app + '\\' + self.app_name + '-' + i
                devicedir = os.path.exists(path_device)

                if devicedir:
                    # print ("File exist!")
                    pass
                else:
                    os.mkdir(path_device)

                file_cmd = self.path_app + '\\' + i + '- ' + '.cmd'
                wl = open(file_cmd, 'w')

                wl.write(
                    'adb -s ' + self.ds[ds_i] + ' logcat -v time *:W > ' + path_device + '\\logcat_%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%.txt\n')
                wl.close()

                # monkey脚本文件
                file_cmd = self.path_app + '\\' + i + '.cmd'
                # 通用monkey命令
                # 指定系统事件百分比
                syskeys = 1
                # 调整触摸事件的百分比
                touch = 75
                # 调整动作事件的百分比
                motion = 14
                # 指定Activity启动的百分比
                appswitch = 0
                # 指定其他事件的百分比
                anyevent = 10
                # 在事件之间插入特定的延时时间
                throttle = 300
                cmd_s = 'adb -s {} shell monkey -p {} --monitor-native-crashes --ignore-crashes --pct-syskeys {} --pct-touch {} --pct-appswitch {} --pct-anyevent {} --pct-motion {} --throttle {} -s %random% -v 20000 > {}\\monkey_%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%.txt\n'.format(
                    self.ds[ds_i], self.app_name, syskeys, touch, motion, appswitch, anyevent, throttle,path_device)
                if self.testmodel.strip() > '0' and self.testmodel.isalnum():
                    self.testmodel = str(int(self.testmodel) + 1)
                    wd = open(file_cmd, 'w')
                    wd.write('data /t && time /t')
                    wd.write(':loop')
                    wd.write('\nset /a num+=1')
                    wd.write('\nif "%num%"=="' + self.testmodel + '" goto end')
                    wd.write('\n' + cmd_s)
                    wd.write('@echo 测试成功完成，请查看日志文件~')
                    wd.write('\nadb -s ' + self.dev + ' shell am force-stop ' + self.app_name)
                    wd.write('\n@ping -n 15 127.0.0.1 >nul')
                    wd.write('\ngoto loop')
                    wd.write('\n:end')
                    wd.close()
                else:
                    print("input type error！")
                ds_i +=1

    def RunMonkey(self,*args,**kwargs):
        '''
        运行入口
        :return:
        '''
        self.CreateMonkeyFile()
        for file in os.listdir(self.path_app):
            if os.path.isfile(os.path.join(self.path_app, file)) == True:
                if file.find('.cmd') > 0:
                    os.system('start ' + os.path.join(self.path_app, '"' + file + '"'))  # dos命令中文件名如果有空格，需加上双引号
                    time.sleep(4)


if __name__ == '__main__':
    pm = PyMonkey()
    pm.RunMonkey()
