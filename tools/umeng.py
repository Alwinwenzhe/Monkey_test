from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, random

class UMeng(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://passport.umeng.com/login")
        # self.driver.maximize_window()
        time.sleep(8)

    def random_time(self):
        '''
        随机休息
        :param wait_time:
        :return:
        '''
        time.sleep(random.randint(2,4))

    def febi(self,id,*args,**kwargs):
        '''
        简化
        :return:
        '''
        self.ob = self.driver.find_element_by_id(id)
        return self.ob

    def febn(self,name,*args,**kwargs):
        return self.driver.find_element_by_name(name)

    def febx(self,xpath,*args,**kwargs):
        self.random_time()
        return self.driver.find_element_by_xpath(xpath)

    def wait_ele_id(self,para):
        '''
        通过id等待对象出现
        :return:
        '''
        try:
            ob = WebDriverWait(self.driver,8).until(EC.presence_of_all_element_located((By.ID,para)))
        except NoSuchElementException as e:
            print(e)
        finally:
            return ob

    def wait_ele_xpath(self,para):
        '''
        通过xpath等待对象出现
        :return:
        '''
        try:
            ob = WebDriverWait(self.driver,20).until(EC.presence_of_all_element_located((By.XPATH,para)))
        except NoSuchElementException as e:
            print(e)
        return ob

    def um_login(self,*args,**kwargs):
        '''
        登录模块
        :param args:
        :param kwargs:
        :return:
        '''
        # 登录
        self.driver.switch_to.frame('alibaba-login-box')
        self.febx('//*[@id="fm-login-id"]').send_keys("chenwenzhecd")
        self.febx('//*[@id="fm-login-password"]').send_keys('123456ab!@')

        # 检验滑块
        drag_slider = self.wait_ele_xpath('//*[@id="nc_1_n1z"]')
        if drag_slider:
            # 获取元素宽度
            drag_slider_width = drag_slider.size
            print(drag_slider_width)
            # 创建一个新的ActionChains，将webdriver实例对driver作为参数值传入，然后通过WenDriver实例执行用户动作
            action_chains = ActionChains(self.driver)
            # 拖动
            action_chains.drag_and_drop_by_offset(drag_slider,drag_slider_width,0).perform()
            time.sleep(3)
        self.febx('//*[@id="fm-login-submit"]').click()

        # 自查通知
        notice = self.wait_ele_xpath('//*[@id="popup-back"]/div/div[3]/button')
        notice.click()

        # 跳转概览
        self.driver.get("https://apm.umeng.com/platform/60c2df8be044530ff0a15611/overview")

        # 第二个自查
        self.wait_ele_xpath('//*[@id="popup-back"]/div/div[3]/button').click()
        crash = self.wait_ele_xpath('//*[@id="umui-layout-scroll"]/section/main/div/div[2]/div[1]/div[2]/div[1]').text
        print(crash)

        # 判定异常值
        if crash > 0:
            print('测试异常，截图，并通过邮件发送日志')


if __name__ == '__main__':
    um = UMeng()
    um.um_login()

