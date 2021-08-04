import time,random

class Com(object):

    def random_time(wait_time=1):
        '''
        随机休息1到指定范围内的数字，单位s
        :param wait_time:
        :return:
        '''
        rand_time = random.randint(1,wait_time)
        time.sleep(rand_time)


if __name__ == '__main__':
    cm = Com()
    cm.random_time()