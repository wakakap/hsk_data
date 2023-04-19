from selenium.webdriver.common.by import By
import time
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from simplefun import message_box, writecsv

def choosedate(driver, datestr):
    try:
        wait = WebDriverWait(driver, 4)
        time_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id$='_time']")))
        time_element.click()
    except Exception as e:
        message_box("error: " + str(e))

    wait = WebDriverWait(driver, 3)
    yearelement = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[lay-type='year']")))
    yearelement.click()
    yearelement2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"li[lay-ym='{datestr[:4]}']")))
    yearelement2.click()
    monthelement = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[lay-type='month']")))
    monthelement.click()
    monthelement2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"li[lay-ym='{str(int(datestr[5:6])-1)}']")))
    monthelement2.click()
    datt = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'td[lay-ymd="{datestr}"]')))
    datt.click()
    time.sleep(1)
    message_box("finish date")

# 我不能很好地定位元素，所以本函数中有很多常数用于微调，可能因设备不同而不同
def movemouse_inwin(positxt, element, canvas_element):
    # 将鼠标移到画布元素左中位置
    canvas_left, canvas_top, canvas_width, canvas_height = canvas_element.location['x'], canvas_element.location['y'], canvas_element.size['width'], canvas_element.size['height']
    mouse_x, mouse_y = canvas_left, canvas_top + canvas_height // 2
    pyautogui.moveTo(translocation(mouse_x, mouse_y))
    x = translocation(mouse_x, mouse_y)[0]
    y = translocation(mouse_x, mouse_y)[1]

    step = 15
    # 缓慢地将鼠标向右移动，同时检测下一个元素的变化

    previous_element_text = ""
    endp = translocation(mouse_x, mouse_y)[0] + canvas_width + 170
    while x <= endp:
        pyautogui.moveTo(x,y)
        # 等待一段时间，以便文本区域更新
        time.sleep(0.001)
        if previous_element_text != canvas_element.text:
            previous_element_text = canvas_element.text
            # message_box("find canvas_element: " + str(previous_element_text))
            # 将新文本写入CSV文件
            row = (positxt+"\n"+ element.text+"\n"+ previous_element_text).split('\n')
            writecsv(row)

        # 平移鼠标
        x = x + step

def closewin(driver):
    try:
    # 关闭窗口
        while True:
            closebuttons = driver.find_elements(By.CLASS_NAME, "layui-layer-close")
            # 如果只有一个窗口——水文站窗口，则跳出
            # 如果没有窗口，则跳出。这种情况是水文站窗口也没了，保险起见加上
            if len(closebuttons) == 1 or len(closebuttons) == 0:
                break
            for i, close_button in enumerate(closebuttons):
                time.sleep(0.1)
                if i == 0:
                    continue
                close_button.click()
    except Exception as e:
        message_box("关闭错误")
        message_box(str(e))


def translocation(browser_x, browser_y):
    # 获取显示器的宽度和高度
    screen_width, screen_height = pyautogui.size()

    # 计算屏幕坐标
    screen_x = browser_x
    screen_y = browser_y

    return screen_x+120, screen_y+140

def findwin(driver,element):
    count = 0
    while True:
        try:
            wait = WebDriverWait(driver, 2)
            canvas_element = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[class*='-r-charts'] canvas")))
            message_box("找到了canvas_element -r-charts")
            break
        
        except:
            try: 
                canvas_element = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-zr-dom-id='zr_0']")))
                message_box("找到了canvas_element zr_0")
                break
            except:
                if count >= 6:
                    message_box("已经尝试了 6 次，仍然无法找到元素")
                    element.click()
                    break

                message_box("no both try scroll")
                count += 1
                pyautogui.scroll(-100)
                time.sleep(1)
                pyautogui.click(button='left')
                continue

    return canvas_element