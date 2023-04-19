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
    if str(element.text) not in filter_text_list:
        message_box("检测到已经做过: " + str(element.text))
        continue

    message_box("开始做: "+ element.text)

    # 获取经纬度
    onclick_value = element.get_attribute("onclick")
    positxt = str(onclick_value)
    
    element.click()
    time.sleep(5)
    try:
        screenWidth, screenHeight = pyautogui.size() # 获取屏幕的尺寸
        pyautogui.moveTo(screenWidth / 2, 5 + screenHeight / 2)
        pyautogui.click(button='left')

        # 水文站点击生成的窗口
        canvas_element = findwin(driver,element)

        dates = ['2022-6-11', '2022-6-12', '2022-6-13', '2022-6-14', '2022-6-15', '2022-6-16']
        
        choosedate(driver, "2022-6-11")# 因为日期连续，这里把前面的操作先做一遍，之后只用找日期框和最后日期

        for date in dates:
            wait = WebDriverWait(driver, 3)
            time_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id$='_time']")))
            time_element.click()
            datt = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'td[lay-ymd="{date}"]')))
            datt.click()
            try:
                message_box("find r-charts again")
                canvas_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[class*='-r-charts']")))
            except:
                message_box("second find zr_0")
                canvas_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-zr-dom-id="zr_0"]')))
            
            #平移鼠标并写csv的操作
            movemouse_inwin(positxt, element, canvas_element)

        # 写下已完成的内容
        with open('./done.txt', 'a',encoding="utf-8") as f:
            f.write(element.text + ',')

        # 关闭窗口
        closewin(driver)

    except Exception as e:
        message_box("出现问题: " + str(element.text))
        message_box(e)
        # 如果有一个问题，就关闭这个窗口，继续下一个
        closewin(driver)
        continue


message_box("main.py全部完成")
# 关闭浏览器
driver.quit()
