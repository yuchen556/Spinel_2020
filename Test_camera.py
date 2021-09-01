import cv2
import numpy as np

import time
# gray = cv2.cvtColor(to_gray_1, cv2.COLOR_BGR2GRAY)
adaptive_threshold1 = cv2.imread(r"C:\Users\Zhen Wang\Documents\Spinel\Test data\saveImage.jpg")
adaptive_threshold = cv2.cvtColor(adaptive_threshold1, cv2.COLOR_BGR2GRAY)
# adaptive_threshold = np.asarray(adaptive_threshold)
# cv2.imwrite('saveImage.jpg', adaptive_threshold)
cv2.imshow("EE", adaptive_threshold)
cv2.waitKey()
# 显示图片的行、列数，以及计算总的灰度值
print("图片行数:" + str(adaptive_threshold.shape[0]))
print("图片列数:" + str(adaptive_threshold.shape[1]))

log_in_grayscale_value = 0

for ii_1 in range(0, adaptive_threshold.shape[0]):
    for jj_1 in range(0, adaptive_threshold.shape[1]):
        pixel = adaptive_threshold.item(ii_1, jj_1)
        log_in_grayscale_value = log_in_grayscale_value + pixel
# 图片灰度总和的，正确值是：468690 or 698445

print("图片灰度总和：" + str(log_in_grayscale_value))