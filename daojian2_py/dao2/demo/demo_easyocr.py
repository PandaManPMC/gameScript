# C:/Users\Administrator\Documents\py_script\dashicunlaogou.png
import cv2
from easyocr import Reader

# 指定模型存储路径
model_storage_directory = './models'

# 初始化 OCR 读取器
reader = Reader(['ch_sim'], gpu=False, model_storage_directory=model_storage_directory)

# 测试图片路径
image_path = 'C:/Users/Administrator/Documents/py_script/yanzhengma.bmp'
image = cv2.imread(image_path)
# 转为灰度图
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 二值化
_, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
# 执行 OCR
result = reader.readtext(binary_image)

# 输出识别结果
for detection in result:
    print(f"文字: {detection[1]}, 置信度: {detection[2]:.2f}")

