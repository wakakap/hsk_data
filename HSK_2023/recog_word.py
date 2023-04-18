import cv2
import pytesseract
import pyautogui
import numpy

# 设置Tesseract OCR引擎的路径
pytesseract.pytesseract.tesseract_cmd = r"E:\CODE\PY\HSK_2023\tesseract-ocr-w64-setup-5.3.1.20230401.exe"

# 截取屏幕上指定区域的图像
x, y, width, height = 100, 100, 200, 200
screenshot = pyautogui.screenshot(region=(x, y, width, height))

# 将PIL图像转换为OpenCV图像
image = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2BGR)

# 对图像进行预处理
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# 使用Tesseract OCR识别图像中的文本
text = pytesseract.image_to_string(threshold_image)

# 在控制台输出识别的文本内容
print(text)

# 如果文本与目标字符串匹配，则获取其坐标并传递给pyautogui
target_string = "example"
if target_string in text:
    coordinates = pyautogui.locateOnScreen(screenshot)
    pyautogui.click(coordinates)  # 在目标文本区域点击鼠标
