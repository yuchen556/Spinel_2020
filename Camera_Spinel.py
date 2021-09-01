# 说明：
# initial_camera_of_1920_1080， 这个函数使用在是否捕捉到log in的界面。
# capture_log_in_UI， 这个函数确认是否捕捉到log in 的界面。
#
# capture_usb_boot_option， 这个函数确认Sandisk U盘在哪一行。
# initial_camera_of_1280_720， 这个函数用在了detect Sandisk U-盘时。
#
# release_camera，这个函数释放视像头
# capture_BYOBIOS_photo_F1, 这个函数没有再使用。改变了测试方案。
#
import cv2
import re
import numpy as np
import pytesseract
import time



# Remove space from string function
def remove_space(string):
    pattern = re.compile(r'\s+')
    return re.sub(pattern, '', string)

def initial_camera_of_1280_720():
    # Pre-photo recognized list
    # camera pre-config
    # camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # 使用下面的设置，会有一个 warning
    time.sleep(10)
    cv2.VideoCapture(0).release()
    time.sleep(10)
    camera = cv2.VideoCapture()
    camera.open(0, cv2.CAP_DSHOW)

    time.sleep(10)
    codec = 0x47504A4D  # MJPG


    camera.set(cv2.CAP_PROP_FPS, 15.0)  # 30 frame per second
    camera.set(cv2.CAP_PROP_FOURCC, codec)  #
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # resolution
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # resolution
    # 下面这个sleep 很重要，没有这个2s，会得到黑屏。
    time.sleep(5)

    if camera.isOpened():
        return_temp, picture = camera.read()
        time.sleep(1)

        if picture.size == 0:
            print("Attempt 1st, initialize camera error！")
        else:
            print("Attempt 1st, initialize camera successfully!")
            # cv2.imwrite('saveImage.jpg', picture)
            # cv2.imshow('1ee', picture)
            # cv2.waitKey()
            return camera

    else:
        print("Camera is not open! 请插拔：_视频采集卡_&_键盘模拟器_！ ")
        quit()

def initial_camera_of_1920_1080():
    # Pre-photo recognized list
    # camera pre-config
    # camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # 使用下面的设置，会有一个 warning
    time.sleep(1)
    cv2.VideoCapture(0).release()
    time.sleep(3)
    camera = cv2.VideoCapture()
    camera.open(0, cv2.CAP_DSHOW)
    time.sleep(2)
    codec = 0x47504A4D  # MJPG
    camera.set(cv2.CAP_PROP_FPS, 15.0)  # 30 frame per second
    camera.set(cv2.CAP_PROP_FOURCC, codec)  #
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # resolution
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # resolution
    # 下面这个sleep 很重要，没有这个2s，会得到黑屏。
    time.sleep(2)

    if camera.isOpened():
        return_temp, picture = camera.read()
        time.sleep(1)

        if picture.size == 0:
            print("Attempt 1st, initialize camera error！")
        else:
            print("Attempt 1st, initialize camera successfully!")
            # cv2.imwrite('saveImage.jpg', picture)
            # cv2.imshow('1ee', picture)
            # cv2.waitKey()
            return camera

        return_temp1, picture1 = camera.read()
        time.sleep(1)

        if picture1.size == 0:
            print("Attempt 2ed, initialize camera error！")
        else:
            print("Attempt 2ed, initialize camera successfully!")
            return camera
    else:
        print("Camera is not open! 请插拔：_视频采集卡_&_键盘模拟器_！ ")
        quit()


def capture_BYOBIOS_photo_F1(camera):

    if camera.isOpened():

        for i in range(300):
            # read camera's image, 是否已经读到。以前没有判断，会导致一个报错：cv2.cvtColor 这个函数error，因为没有捕捉到。
            time.sleep(0.1)
            return_value, img = camera.read()

            if return_value == 1:
                to_gray = img
                cv2.imwrite('1st time.jpg', to_gray)
                cv2.imshow('ee', to_gray)
                cv2.waitKey()

            else:
                return_value1, img1 = camera.read()
                if return_value1 == 1:
                    to_gray = img1

                else:
                    print("Can't capture the photo! 请插拔：_视频采集卡_&_键盘模拟器_！ ")
                    quit()

            time.sleep(0.1)
            # color convert
            # img = cv2.resize(img, None, fx=0.8, fy=0.8)
            to_gray_1 = to_gray[100:250, 180:500]
            # cv2.imshow("EE", to_gray_1)
            # cv2.waitKey()
            gray = cv2.cvtColor(to_gray_1, cv2.COLOR_BGR2GRAY)
            # adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,1)
            text = pytesseract.image_to_string(gray, lang='chi_sim')
            string = remove_space(text)
            fullstring = string
            substring = "过当前页面"

            if substring in fullstring:
                print("found this picture!")
                break
            else:
                print("Not found!{}".format(i))
    else:
        print("camera error")


def capture_usb_boot_option(camera):


    # isOpened() 用来检查 摄像头初始化是否成功
    if camera.isOpened():
        for i in range(2):
            # read camera's image
            return_value, img = camera.read()
            if return_value == 1:
                to_gray = img

            else:
                return_value1, img1 = camera.read()
                if return_value1 == 1:
                    to_gray = img1

                else:
                    print("Can't capture the photo! 请插拔：_视频采集卡_&_键盘模拟器_！ ")
                    quit()

            time.sleep(0.1)
            # 将图像转成灰度
            gray = cv2.cvtColor(to_gray, cv2.COLOR_BGR2GRAY)
            # 再将灰度图片做‘反二值化 阈值处理’ （具体可参考 P133 《OpenCV 轻松入门面向Python》）
            t, T_threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
            # 抽取图像中的行、列（行从220 到500， 列从260 到700）（具体可参考 P29 《OpenCV 轻松入门面向Python》）
            T1_threshold = T_threshold[240:460, 370:890]
            # 使用google pytesseract 抽取图片里的英文文字
            text = pytesseract.image_to_string(T1_threshold, lang='eng')
            # cv2.imshow("ttt3456", T1_threshold)
            # cv2.waitKey()
            cv2.imwrite('tttt-01.jpg', T1_threshold)
            print(text)
            # 除去字符串里的空白行（不包含有空格的行）
            string1 = text.replace('\n\n', '\n')
            # The lstrip() method removes any leading characters (space is the default leading character to remove)
            string2 = string1.lstrip()
            # The rstrip() method removes any trailing characters (characters at the end a string), space is the default trailing character to remove.
            string3 = string2.rstrip()

            # string3 = string3.split("\n", 7)[7]
            print(string3)
            # 计算这个string 有几行
            Boot_device_qty = len(string3.splitlines())
            print(Boot_device_qty)
            full_string = string3

            # 下面for循环,得到SanDisk 这个单词在第几行
            row_number = 1
            for item in full_string.split("\n"):
                if "SanDisk" in item:
                    sandisk_at_row = row_number
                    # print("U_Disk locate at {} row".format(row_sandisk))
                    break
                row_number = row_number + 1

            print(row_number)
            return (row_number, Boot_device_qty)
            # print(row_sandisk)
            # print(Eddy_Rows)
            # print(full_string)
            # cv2.imshow("ttt", T1_threshold)
            # cv2.waitKey()
            # cv2.imwrite('tttt.jpg', T1_threshold)

    else:
        print("camera error")


def capture_log_in_UI(camera):
    time.sleep(2)
    capture_log_in_num = 0

    if camera.isOpened():

        for i in range(2):
            # read camera's image, 是否已经读到。以前没有判断，会导致一个报错：cv2.cvtColor 这个函数error，因为没有捕捉到。
            time.sleep(0.1)
            return_value, img = camera.read()

            if return_value == 1:
                to_gray = img
            else:
                return_value1, img1 = camera.read()
                if return_value1 == 1:
                    to_gray = img1
                else:
                    print("Can't capture the photo! 请插拔：_视频采集卡_&_键盘模拟器_！ ！")
                    quit()

            time.sleep(0.1)
            # color convert
            # img = cv2.resize(img, None, fx=0.8, fy=0.8)

            to_gray_1 = to_gray[650:770, 712:1200]

            # 转换成灰度图片
            gray = cv2.cvtColor(to_gray_1, cv2.COLOR_BGR2GRAY)

            # adaptive_threshold = cv2.adaptiveThreshold(gray, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,1)
            # 将图片进行阈值处理，大于50 的都变为 255.
            t, adaptive_threshold = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
            cv2.imwrite('saveImage.jpg', adaptive_threshold)
            # cv2.imshow("EE", adaptive_threshold)
            # cv2.waitKey()
            # 显示图片的行、列数，以及计算总的灰度值
            print("图片行数:" + str(adaptive_threshold.shape[0]))
            print("图片列数:" + str(adaptive_threshold.shape[1]))

            log_in_grayscale_value = 0
            for ii1 in range(0, adaptive_threshold.shape[0]):
                for jj1 in range(0, adaptive_threshold.shape[1]):
                    pixel = adaptive_threshold.item(ii1, jj1)
                    log_in_grayscale_value = log_in_grayscale_value + pixel
            # 图片灰度总和的，正确值是：468690 or 698445
            print("图片灰度总和：" + str(log_in_grayscale_value))

            Judgement_gray_value1 = ((log_in_grayscale_value >400000) and (log_in_grayscale_value < 700000))
            # Judgement_gray_value2 = ((log_in_grayscale_value > 698300) and (log_in_grayscale_value < 698600))

            if Judgement_gray_value1:
                print("Captured log in screen.")
                break
            else:
                capture_log_in_num = capture_log_in_num + 1
                if capture_log_in_num == 1:
                    print("Attempt {} times\n".format(i))
                else:
                    print("请插拔：_视频采集卡_&_键盘模拟器_！ Camera Not found log in screen!{}\n".format(i))
                    quit()

    else:
        print("camera error")


def release_camera(camera):
    time.sleep(1)
    camera.release()
    del (camera)
    cv2.destroyAllWindows()

