from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function import closewin, message_box, findwin, choosedate, movemouse_inwin
from simplefun import writelist,filterlist
from selenium.webdriver.common.action_chains import ActionChains

# 从txt文件中读取cookie信息
def load_cookie_from_txt(txt_file):
    with open(txt_file, 'r') as f:
        # 从txt文件中读取cookie字符串
        cookie_str = f.read()
        # 将cookie字符串转换成字典形式
        cookie_dict = {i.split('=')[0]:i.split('=')[1] for i in cookie_str.split(';') if i.strip()}
        return cookie_dict

# 创建 Chrome 浏览器的 WebDriver 对象
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

# 打开
driver.get("https://www.nhhb.org.cn/nbwebgis/")

# 手动登陆
# ---------------------
time.sleep(20)

# 获取当前页面的所有cookie
cookies = driver.get_cookies()
# 将cookie写入txt文件
with open('cookies.txt', 'w', encoding="utf-8") as f:
    for cookie in cookies:
        # 只保留必要信息，即name和value
        cookie_str = '{}={};'.format(cookie['name'], cookie['value'])
        f.write(cookie_str)
# ------------------------

# cookies = load_cookie_from_txt('cookies.txt')
# for k,v in cookies.items():
#     # 添加cookie
#     driver.add_cookie({'name':k, 'value':v})
#     message_box("加载 cookie: " + k + " " + v)
# # 刷新页面
# driver.refresh()

time.sleep(3)
try:
    action = ActionChains(driver)
    bar = driver.find_element(By.LINK_TEXT, "航保设施")
    # 创建ActionChains对象
    # 将鼠标移动到元素上
    action.move_to_element(bar)
    action.perform()
except Exception as e:
    message_box("航保设施bar 失败 退出")
    message_box("error: " + str(e))
    driver.quit()


try:
    action = ActionChains(driver)
    bar2 = driver.find_element(By.LINK_TEXT, "水文站")
    action.move_to_element(bar2)
    action.click()
    action.perform()
except Exception as e:
    message_box("水文站bar 失败 退出")
    message_box("error: " + str(e))
    driver.quit()

try:
# 找到所有水文站
    time.sleep(2)
    wait = WebDriverWait(driver, 5)
    elements = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"a[onclick^='locatSwz']")))
    time.sleep(3)#有时候表格会分两次加载出来所以我再找一次
    elements = driver.find_elements(By.CSS_SELECTOR,"a[onclick^='locatSwz']")
    message_box("find elements: " + str(len(elements)))
except Exception as e:
    message_box("error: " + str(e))
    message_box("水文站列表获取失败，准备关闭浏览器")
    driver.quit()

text_list = [element.text for element in elements]
# 写入水文站列表
import os
if not os.path.exists("shuiwenzhan.txt"):
    writelist(text_list)

filter_text_list = filterlist(text_list) # 要做的水文站列表
message_box("after filter elementlen: " + str(len(filter_text_list)))

for element in elements:
    element.click()
    wait = WebDriverWait(driver, 2)
    posi = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ol-mouse-position-me')))
    positxt = posi.text.replace('\n', ',')

    with open('./经纬度对应表.txt', 'a',encoding="utf-8") as f:
            f.write(element.text + ':'+positxt + '\n')



message_box("main.py全部完成")
# 关闭浏览器
driver.quit()
