import cv2
from paddleocr import PaddleOCR
import matplotlib.pyplot as plt

# image_path = 'C:/Users/Administrator/Documents/py_script/yanzhengma.bmp'
# image_path = 'C:/Users/Administrator/Documents/py_script/dashicunlaogou.png'
image_path = 'C:/Users/Administrator/Documents/py_script/person.bmp'


# 1. 读取图片
image = cv2.imread(image_path)

# 2. 转为灰度图
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 3. 去噪（高斯模糊）
# blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# 4. 自适应二值化处理
# binary_image = cv2.adaptiveThreshold(
#     blurred_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 3
# )

# 5. 增强对比度
# enhanced_image = cv2.equalizeHist(blurred_image)

# 保存处理后的图片用于检查
processed_image_path = 'processed_image.bmp'
cv2.imwrite(processed_image_path, gray_image)

# 显示处理后的图片
# plt.imshow(enhanced_image, cmap='gray')
# plt.title("Processed Image")
# plt.axis('off')
# plt.show()

# 6. 使用 PaddleOCR 进行中文识别
ocr = PaddleOCR(use_angle_cls=True, lang='ch')
result = ocr.ocr(processed_image_path, cls=True)

# 7. 输出识别结果
print("识别结果:")
for line in result[0]:
    print(f"文字: {line[1][0]}, 置信度: {line[1][1]:.2f}")
