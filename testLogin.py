from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.maximize_window()

browser.get("https://tieba.baidu.com/index.html")

browser.find_element_by_xpath('//*[@id="com_userbar"]/ul/li[4]/div/a').click()
time.sleep(3)

browser.find_element_by_xpath(
    '//*[@id="TANGRAM__PSP_10__footerULoginBtn"]').click()
time.sleep(5)

username = '天时的天使11'
password = '93.10.08'

browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__userName"]').send_keys(
    username)
browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__password"]').send_keys(
    password)

browser.find_element_by_xpath('//*[@id="TANGRAM__PSP_10__submit"]').click()

time.sleep(2)
browser.find_element_by_xpath('//*[@id="onekey_sign"]/a').click()

time.sleep(2)
browser.find_element_by_xpath('//*[@id="dialogJbody"]/div/div/div[1]/a').click()