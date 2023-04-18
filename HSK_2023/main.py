from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from function import closewin, message_box, findwin, choosedate, movemouse_inwin
from simplefun import writelist,filterlist

# 创建 Chrome 浏览器的 WebDriver 对象
driver = webdriver.Chrome()

# 访问目标网页
driver.get("https://www.nhhb.org.cn/nbwebgis/")

time.sleep(15)

browser_info = driver.execute_script("return [window.screenX, window.screenY, window.outerWidth, window.outerHeight];")
browser_x, browser_y, browser_width, browser_height = browser_info
screenWidth, screenHeight = pyautogui.size()

# 找到所有水文站
elements = driver.find_elements(By.CSS_SELECTOR,"a[onclick^='locatSwz']")
message_box("find elements: " + str(len(elements)))

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

    element.click()
    time.sleep(5)

    try:
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
            movemouse_inwin(element, canvas_element)

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

# 关闭浏览器
driver.quit()
