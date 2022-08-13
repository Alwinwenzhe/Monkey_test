import os


def get_files(self, root_path, file_list):
    '''
    递推获取所有文件，返回文件名
    :return:
    '''
    files = root_path
    dir_list = os.listdir(files)  # 获取该目录下所有文件
    for file in dir_list:
        if os.path.isdir(file):  # 判断文件是否是目录
            file_list.append(file)
            get_files(root_path, file_list)
        elif not file.endwith('cmd'):
            pass
            # 这里调用遍历日志方法

class CheckLog(object):

    def get_file_path(self):
        '''
        获取文件路径
        :return:
        '''
        proj_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) # 绝对路径
        report_path = os.path.join(proj_path,'bugreport_out')
        return report_path

    def check_log(self,file):
        '''
        获取文件中，log是否正确
        :return:
        '''
        with open(file,'a') as f:
            content = f.readlines()
        # 对内容进行正则过滤



if __name__ == '__main__':
    cl =CheckLog()
    print(cl.get_file_path())