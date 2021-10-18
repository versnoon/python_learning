#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sel.py
@Time    :   2021/06/17 13:43:59
@Author  :   Tong tan
@Version :   1.0
@Contact :   tongtan@gmail.com
'''


import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep


if __name__ == '__main__':
    driver = webdriver.Ie()
    driver.get('http://ehr.baogang.info/hs/')
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
    # 输入用户名
    driver.find_element_by_id('username').send_keys('M73677')
    # 输入密码
    driver.find_element_by_id('password').send_keys('tongtan0001')
    # 点击登录
    driver.find_element_by_class_name('loginbtn1').click()
    sleep(6)
    # 选择控制台
    driver.find_element_by_class_name('icon6').click()
    sleep(6)
    # 切换iframe
    driver.switch_to.frame('frontFrm')
    # 选择集团本部
    driver.find_element_by_xpath('//input[@value="1"]').click()

    # 页面跳转
    driver.switch_to.window(driver.window_handles[0])

    # 切换iframe
    driver.switch_to.frame(driver.find_element_by_id('mainScreenFrm'))

    # 悬停菜单
    salary_menu = driver.find_element_by_link_text('薪酬管理 ▽')
    ActionChains(driver).move_to_element(salary_menu).perform()
    gz_ele = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@id='nav_bar']/div/ul/li/ul/li/a[text()='工资管理           >']")))
    sleep(1)
    # 移动到工资管理
    ActionChains(driver).move_to_element(gz_ele).perform()
    # 点击工资计算
    gz_cal_click = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@id='nav_bar']/div/ul/li/ul/li/ul//li/a[text()='工资计算']")))
    sleep(1)
    gz_cal_click.click()
    print('end')
