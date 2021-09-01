# https://datatofish.com/entry-box-tkinter/
import tkinter as tk
import Search_SN
import MAC_TO_Array
import PLC
import Camera_Spinel
import Keyboard_Function
import ssh_shell
import logging
import smtplib
import ssl
import os
from os import path
import cv2
import re
import numpy as np
import pytesseract
import time
from datetime import datetime


# 检查还剩余多少free 的MAC地址
available_mac_address = Search_SN.search_free_mac()
print(available_mac_address)
min_number = 10

if available_mac_address >= min_number:
    # 调用图形界面
    root = tk.Tk()
    # 图形界面的大小 400*300
    canvas1 = tk.Canvas(root, width=1080, height=720, relief='raised')
    canvas1.pack()
    # 图形界面里显示的文字、及位置-1
    label1 = tk.Label(root, text='Spinel Test Platform')
    label1.config(font=('helvetica', 35))
    canvas1.create_window(540, 100, window=label1)
    # 图形界面里显示的文字、及位置-2
    label11 = tk.Label(root, text='Free MAC has {} item left.'.format(available_mac_address))
    label11.config(font=('helvetica', 15))
    canvas1.create_window(540, 150, window=label11)

    # 图形界面里显示的文字、及位置
    label2 = tk.Label(root, text='请扫描条形码, 然后点击Testing 按钮！')
    label2.config(font=('helvetica', 25))
    canvas1.create_window(540, 300, window=label2)
    # 图形界面里SN 的输入框、及位置
    entry1 = tk.Entry(root)
    canvas1.create_window(540, 400, window=entry1)


    # 点击button，运行get_spinel_sn()函数:
    def get_spinel_sn():
        global spinel_sn
        spinel_sn = entry1.get()

        # 若sn 是13位的，则使输入框disable.
        if (len(spinel_sn) == 13) and (spinel_sn.isnumeric()):
            t1 = time.time()
            # 图形界面里显示的文字
            label3 = tk.Label(root, text='SN of this board is:', font=('helvetica', 10))
            canvas1.create_window(200, 210, window=label3)

            label4 = tk.Label(root, text=spinel_sn, font=('helvetica', 20, 'bold'))
            canvas1.create_window(200, 250, window=label4)
            # 图形界面里button 变为绿色，输入框变为不能输入
            button1.configure(background="green")
            entry1.config(state='disabled')

            # Log_File: check the previous broken log file existed or not.
            if path.exists(r'C:\Users\Zhen Wang\Desktop\0211_test_log\20212021.log'):
                print("Delete the previous file.")
                os.remove(r'C:\Users\Zhen Wang\Desktop\0211_test_log\20212021.log')
            else:
                print("No file existed!")

            time.sleep(2)
            spinel_temp_name = "20212021" + ".log"
            logging.basicConfig(filename=r'C:\Users\Zhen Wang\Desktop\0211_test_log\{:s}'.format(spinel_temp_name),
                                filemode='a',
                                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                datefmt='%Y-%m-%d, %H:%M:%S',
                                level=logging.INFO)
            logging.info(':Start testing')

            # 得到SN所需要的MAC的行数：
            row_address = Search_SN.search_db_sn(spinel_sn)
            print(row_address)
            logging.info('row_address: {}'.format(row_address))
            # 得到10个MAC 地址：
            ten_mac_address = MAC_TO_Array.MAC_adds_TO_Array(row_address)
            for y in ten_mac_address:
                print(y)
                logging.info('MAC_address: {}'.format(y))
            # 找到这10个MAC地址，将每个mac address 拆分成12个键
            # MAC_TO_Key.One_MAC_TO_12Keys(ten_mac_address[0])

        # 第1次启动 系统自检，会自己重启
            print("开始：第1次启动 系统自检，会自己重启")
            logging.info('开始：第1次启动 系统自检，会自己重启')
            PLC.AC_power_off()
            time.sleep(3)
            PLC.AC_power_on()
            time.sleep(2)
            PLC.Button_Power_on_PC()
            time.sleep(120)
            print("结束：第1次启动 系统自检，会自己重启")
            logging.info('结束：第1次启动 系统自检，会自己重启')

        # 第2次启动：将硬盘加密功能-关闭
            print("开始：第2次启动：将硬盘加密功能-关闭")
            logging.info('开始：第2次启动：将硬盘加密功能-关闭')
            PLC.AC_power_off()
            time.sleep(2)
            PLC.AC_power_on()
            time.sleep(5)
            # PLC.Button_Restart_PC()

            # 初始化camera
            print("Send F1")
            logging.info('Send F1')
            Keyboard_Function.bios_f1()
            print("初始化camera_0...")
            logging.info('初始化camera_0...')
            camera_device0 = Camera_Spinel.initial_camera_of_1920_1080()
            print("初始化camera_0 成功！")
            logging.info('初始化camera_0 成功！')

            Camera_Spinel.capture_log_in_UI(camera_device0)
            Camera_Spinel.release_camera(camera_device0)
            Keyboard_Function.secadm_usr()
            Keyboard_Function.secadm_pw()
            Keyboard_Function.Close_HDD_security()
            print("结束：第2次启动：将硬盘加密功能-关闭")
            logging.info('结束：第2次启动：将硬盘加密功能-关闭')

        # 第3次启动：启动项管理开关-打开
            print("开始：第3次启动：启动项管理开关-打开")
            logging.info("开始：第3次启动：启动项管理开关-打开")
            PLC.AC_power_off()
            time.sleep(2)
            PLC.AC_power_on()
            time.sleep(5)
            print("Send F1")
            logging.info("Send F1")
            Keyboard_Function.bios_f1()
            # 初始化camera
            print("初始化camera_1...")
            logging.info("初始化camera_1...")
            camera_device1 = Camera_Spinel.initial_camera_of_1920_1080()
            print("初始化camera_1 成功！")
            logging.info("初始化camera_1 成功！")

            Camera_Spinel.capture_log_in_UI(camera_device1)
            Camera_Spinel.release_camera(camera_device1)
            Keyboard_Function.secadm_usr()
            Keyboard_Function.secadm_pw()
            Keyboard_Function.Open_boot_item()
            print("结束：第3次启动：启动项管理开关-打开")
            logging.info("结束：第3次启动：启动项管理开关-打开")


        # 第4-1次启动：选择U disk 启动
            print("开始：第4-1次启动：选择U disk 启动")
            logging.info("开始：第4-1次启动：选择U disk 启动")

            PLC.AC_power_off()
            time.sleep(2)
            PLC.AC_power_on()
            time.sleep(5)
            print("Send F1")
            logging.info("Send F1")
            Keyboard_Function.bios_f1()

            # 初始化camera
            print("初始化camera_2-1...")
            logging.info("初始化camera_2-1...")
            camera_device3 = Camera_Spinel.initial_camera_of_1920_1080()
            print("初始化camera_2-1 成功！")
            logging.info("初始化camera_2-1 成功！")
            Camera_Spinel.capture_log_in_UI(camera_device3)
            Camera_Spinel.release_camera(camera_device3)
            Keyboard_Function.root_usr()
            Keyboard_Function.root_pw()

            # 进入USB 选项界面
            Keyboard_Function.pre_usb_key_action()

            # 初始化camera
            print("初始化camera_3-1...")
            logging.info("初始化camera_3-1...")
            time.sleep(5)
            camera_device4 = Camera_Spinel.initial_camera_of_1280_720()
            print("初始化camera_3-1 成功！")
            logging.info("初始化camera_3-1 成功！")

            USB_Disk_check, device_quantity = Camera_Spinel.capture_usb_boot_option(camera_device4)
            print(USB_Disk_check, device_quantity)
            logging.info("Sandisk_U_disk_installed_with_Centos_at_:_{}, device_QTY:_{}".format(USB_Disk_check, device_quantity))

            Sandisk = Keyboard_Function.USB_Boot(USB_Disk_check, device_quantity)
            Camera_Spinel.release_camera(camera_device4)
            if Sandisk is True:
                print("4-1Detect the U_disk_Sandisk OS boot")
                logging.info("4-1Detect the U_disk_Sandisk OS boot")
            else:
                print("4-1_Error!!!: can't detect the U_disk_Sandisk OS boot!")
                logging.info("4-1_Error!!!: can't detect the U_disk_Sandisk OS boot! 请确保 U 盘插入正确！")

            print("结束：第4-1次启动：选择U disk 启动")
            logging.info("结束：第4-1次启动：选择U disk 启动")

        # 第5-1次启动：开机关机的目的：workaround for BYO bug issue.

            print("开始：第5-1次启动：workaround for BYO bug issue")
            logging.info("开始：第5-1次启动：workaround for BYO bug issue")
            PLC.AC_power_off()
            time.sleep(2)
            PLC.AC_power_on()
            time.sleep(60)


        # 第4-2次启动：选择U disk 启动
            print("开始：第4-2次启动：选择U disk 启动")
            logging.info("开始：第4-2次启动：选择U disk 启动")

            PLC.AC_power_off()
            time.sleep(2)
            PLC.AC_power_on()
            time.sleep(5)
            print("Send F1")
            logging.info("Send F1")
            Keyboard_Function.bios_f1()

            # 初始化camera
            print("初始化camera_2-2...")
            logging.info("初始化camera_2-2...")
            camera_device3 = Camera_Spinel.initial_camera_of_1920_1080()
            print("初始化camera_2-2 成功！")
            logging.info("初始化camera_2-2 成功！")
            Camera_Spinel.capture_log_in_UI(camera_device3)
            Camera_Spinel.release_camera(camera_device3)
            Keyboard_Function.root_usr()
            Keyboard_Function.root_pw()

            # 进入USB 选项界面
            Keyboard_Function.pre_usb_key_action()

            # 初始化camera
            print("初始化camera_3-2...")
            logging.info("初始化camera_3-2...")
            time.sleep(5)
            camera_device4 = Camera_Spinel.initial_camera_of_1280_720()
            print("初始化camera_3-2 成功！")
            logging.info("初始化camera_3-2 成功！")

            USB_Disk_check, device_quantity = Camera_Spinel.capture_usb_boot_option(camera_device4)
            print(USB_Disk_check, device_quantity)
            logging.info(
                "Sandisk_U_disk_installed_with_Centos_at_:_{}, device_QTY:_{}".format(USB_Disk_check, device_quantity))

            Sandisk = Keyboard_Function.USB_Boot(USB_Disk_check, device_quantity)
            Camera_Spinel.release_camera(camera_device4)
            if Sandisk is True:
                print("4-2_Detect the U_disk_Sandisk OS boot")
                logging.info("4-2_Detect the U_disk_Sandisk OS boot")
            else:
                print("4-2_Error!!!: can't detect the U_disk_Sandisk OS boot!")
                logging.info("4-2_Error!!!: can't detect the U_disk_Sandisk OS boot! 请确保 U 盘插入正确！")

            print("结束：第4-2次启动：选择U disk 启动")
            logging.info("结束：第4-2次启动：选择U disk 启动")



        # 第5-2次启动：开机关机的目的：workaround for BYO bug issue.

            print("开始：第5-2次启动：workaround for BYO bug issue")
            logging.info("开始：第5-2次启动：workaround for BYO bug issue")
            PLC.AC_power_off()
            time.sleep(2)
            PLC.AC_power_on()
            time.sleep(60)

        # 第6次启动：更新所有的预期值
            print("开始：第6次启动：更新所有的预期值")
            logging.info("开始：第6次启动：更新所有的预期值")

            time.sleep(2)
            PLC.AC_power_off()
            time.sleep(50)
            PLC.AC_power_on()
            time.sleep(5)

            print("Send F1")
            logging.info("Send F1")
            Keyboard_Function.bios_f1()

            # 初始化camera
            print("初始化camera_4...")
            logging.info("初始化camera_4...")
            camera_device2 = Camera_Spinel.initial_camera_of_1920_1080()
            print("初始化camera_4 成功！")
            logging.info("初始化camera_4 成功！")

            Camera_Spinel.capture_log_in_UI(camera_device2)
            Camera_Spinel.release_camera(camera_device2)
            Keyboard_Function.secadm_usr()
            Keyboard_Function.secadm_pw()
            Keyboard_Function.update_safety_setting()
            print("结束：第6次启动：更新所有的预期值")
            logging.info("结束：第6次启动：更新所有的预期值")


        # 第7次启动： 通过SSH进入操作系统,更新MAC
            print("开始：第7次启动： 通过SSH进入操作系统,更新MAC")
            logging.info("开始：第7次启动： 通过SSH进入操作系统,更新MAC")
            PLC.AC_power_off()
            time.sleep(40)
            PLC.AC_power_on()
            time.sleep(70)
            Keyboard_Function.Keyboard_send("Send_Enter")
            Keyboard_Function.root_usr()
            Keyboard_Function.root_pw()
            Keyboard_Function.keyboard_right_enter_to_centos()

            mac_1 = ten_mac_address[0]
            mac_5 = ten_mac_address[4]
            mac_7 = ten_mac_address[6]
            tt_sn = '77777' + spinel_sn

            # update 1st
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            ssh_shell.update_enp12s0f0_mac(mac_1, tt_sn, channel_spinel)
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            time.sleep(2)

            # update 2nd
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            ssh_shell.update_enp11s0f0_mac(mac_5, tt_sn, channel_spinel)
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            time.sleep(2)

            # update 3rd
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            ssh_shell.update_enp3s0f0_mac(mac_7, tt_sn, channel_spinel)
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            time.sleep(2)

            print("结束：第7次启动： 通过SSH进入操作系统,更新MAC")
            logging.info("结束：第7次启动： 通过SSH进入操作系统,更新MAC")

        # 第8次启动：更新所有的预期值
            print("开始：第8次启动：更新所有的预期值")
            logging.info("开始：第8次启动：更新所有的预期值")
            time.sleep(5)
            PLC.AC_power_off()
            time.sleep(50)
            PLC.AC_power_on()
            time.sleep(10)

            print("Send F1")
            logging.info("Send F1")
            Keyboard_Function.bios_f1()

            # 初始化camera
            print("初始化camera_5...")
            logging.info("初始化camera_5...")
            camera_device6 = Camera_Spinel.initial_camera_of_1920_1080()
            print("初始化camera_5 成功！")
            logging.info("初始化camera_5 成功！")

            Camera_Spinel.capture_log_in_UI(camera_device6)
            Camera_Spinel.release_camera(camera_device6)
            Keyboard_Function.secadm_usr()
            Keyboard_Function.secadm_pw()
            Keyboard_Function.update_safety_setting()
            print("结束：第8次启动：更新所有的预期值")
            logging.info("结束：第8次启动：更新所有的预期值")

        # 第9次启动： 通过SSH进入操作系统,测试Spinel
            print("开始：第9次启动： 通过SSH进入操作系统,测试Spinel ")
            logging.info("开始：第9次启动： 通过SSH进入操作系统,测试Spinel ")
            PLC.AC_power_off()
            time.sleep(40)
            PLC.AC_power_on()
            time.sleep(70)
            Keyboard_Function.Keyboard_send("Send_Enter")
            Keyboard_Function.root_usr()
            Keyboard_Function.root_pw()
            Keyboard_Function.keyboard_right_enter_to_centos()



        # 01-1 等待进入系统后，建立链接进行_enp12s0f0_MAC_address_测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            enp12_mac_verify = ssh_shell.t_01_enp12s0f0_mac_verify(channel_spinel, ten_mac_address[0], ten_mac_address[1], ten_mac_address[2], ten_mac_address[3])
            print("enp12s0f0 mac address is:" + str(enp12_mac_verify))
            logging.info("enp12s0f0 mac address is:_{}".format(str(enp12_mac_verify)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_enp12s0f0_MAC_address_结束！")
            logging.info("测试_enp12s0f0_MAC_address_结束！")
            time.sleep(1)

        # 01-2 等待进入系统后，建立链接进行_enp11s0f0_MAC_address_测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            enp11_mac_verify = ssh_shell.t_01_enp11s0f0_mac_verify(channel_spinel, ten_mac_address[4], ten_mac_address[5])
            print("enp11s0f0 mac address is:" + str(enp11_mac_verify))
            logging.info("enp11s0f0 mac address is:_{}".format(str(enp11_mac_verify)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_enp11s0f0_MAC_address_结束！")
            logging.info("测试_enp11s0f0_MAC_address_结束！")
            time.sleep(1)

        # 01-3 等待进入系统后，建立链接进行_enp3s0f0_MAC_address_测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            enp3_mac_verify = ssh_shell.t_01_enp3s0f0_mac_verify(channel_spinel, ten_mac_address[6], ten_mac_address[7], ten_mac_address[8], ten_mac_address[9])
            print("enp3s0f0 mac address is:" + str(enp3_mac_verify))
            logging.info("enp3s0f0 mac address is:_{}".format(str(enp3_mac_verify)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_enp3s0f0_MAC_address_结束！")
            logging.info("测试_enp3s0f0_MAC_address_结束！")
            time.sleep(1)

        # 02-1 进行 ethtool_enp12s0f2测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            enp12s0f2_eth_result = ssh_shell.t_02_1_ethtool_enp12s0f2_(channel_spinel)
            print("enp12s0f2 test resulted is: " + str(enp12s0f2_eth_result))
            logging.info("enp12s0f2 test resulted is:_{}".format(str(enp12s0f2_eth_result)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_ethtool_enp12s0f2_结束！")
            logging.info("测试_ethtool_enp12s0f2_结束！")
            time.sleep(1)

        # 02-2 进行 ethtool_enp12s0f3测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            enp12s0f3_eth_result = ssh_shell.t_02_2_ethtool_enp12s0f3_(channel_spinel)
            print("enp12s0f3 test resulted is: " + str(enp12s0f3_eth_result))
            logging.info("enp12s0f3 test resulted is:_{}".format(str(enp12s0f3_eth_result)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_ethtool_enp12s0f3_结束！")
            logging.info("测试_ethtool_enp12s0f3_结束！")
            time.sleep(1)

        # 02-3 进行 ethtool_enp11s0f1测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            enp11s0f1_eth_result = ssh_shell.t_02_3_ethtool_enp11s0f1_(channel_spinel)
            print("enp11s0f1 test resulted is: " + str(enp11s0f1_eth_result))
            logging.info("enp11s0f1 test resulted is:_{}".format(str(enp11s0f1_eth_result)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_ethtool_enp11s0f1_结束！")
            logging.info("测试_ethtool_enp11s0f1_结束！")
            time.sleep(1)

        # 02-4 进行 ethtool_enp11s0f0测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            enp11s0f0_eth_result = ssh_shell.t_02_4_ethtool_enp11s0f0_(channel_spinel)
            print("enp11s0f0 test resulted is: " + str(enp11s0f0_eth_result))
            logging.info("enp11s0f0 test resulted is:_{}".format(str(enp11s0f0_eth_result)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_ethtool_enp11s0f0_结束！")
            logging.info("测试_ethtool_enp11s0f0_结束！")
            time.sleep(1)

        # 02-5 进行 ethtool_enp3s0f3测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            enp3s0f3_eth_result = ssh_shell.t_02_5_ethtool_enp3s0f3_(channel_spinel)
            print("enp3s0f3 test resulted is: " + str(enp3s0f3_eth_result))
            logging.info("enp3s0f3 test resulted is:_{}".format(str(enp3s0f3_eth_result)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_ethtool_enp3s0f3_结束！")
            logging.info("测试_ethtool_enp3s0f3_结束！")
            time.sleep(1)

        # 03进行 check_BIOS 测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            bios_result = ssh_shell.t_03_check_BIOS_(channel_spinel)
            print("BIOS version is: " + str(bios_result))
            logging.info("BIOS version is:_{}".format(str(bios_result)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_BIOS_结束！")
            logging.info("测试_BIOS_结束！")
            time.sleep(1)

        # 04进行 check_cpu 测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            cpu_result = ssh_shell.t_04_check_cpu_(channel_spinel)
            print("CPU result is: " + str(cpu_result))
            logging.info("CPU result is:_{}".format(str(cpu_result)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_CPU_结束！")
            logging.info("测试_CPU_结束！")
            time.sleep(1)

        # 05进行 check_memory 测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            memory_result = ssh_shell.t_05_check_memory_(channel_spinel)
            print("Memory result is: " + str(memory_result))
            logging.info("Memory result is:_{}".format(str(memory_result)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_Memory_结束！")
            logging.info("测试_Memory_结束！")
            time.sleep(1)

        # 06进行 check_sn 测试。
            # 06-等待进入系统后，建立链接进行_sn_测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            sn_verify, sn_on_wangxun = ssh_shell.t_06_check_spinel_sn(channel_spinel)
            print("Spinel serial number is:" + str(sn_verify) + sn_on_wangxun)
            logging.info("Spinel serial number is:_{}_and SN:{}".format(str(sn_verify), sn_on_wangxun))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_SN_结束！")
            logging.info("测试_SN_结束！")
            time.sleep(1)

        # 07进行 check_disk_&_usb_port 测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            disk_usb_result = ssh_shell.t_07_disk_usb_port_(channel_spinel)
            print("Disk & USB result is: " + str(disk_usb_result))
            logging.info("Disk & USB result is:_{}".format(str(disk_usb_result)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_disk_usb_结束！")
            logging.info("测试_disk_usb_结束！")
            time.sleep(1)

        # 08进行 check_pci_port 测试。
            channel_spinel, ssh_client_spinel = ssh_shell.connect_spinel_ssh()
            pci_e_x4_x8_result = ssh_shell.t_08_check_pci_port_(channel_spinel)
            print("PCI-E x4, x8 ports result are: " + str(pci_e_x4_x8_result))
            logging.info("PCI-E x4, x8 ports result are:_{}".format(str(pci_e_x4_x8_result)))
            ssh_shell.disconnect_ssh(channel_spinel, ssh_client_spinel)
            print("测试_PCI-E x4, x8 结束！")
            logging.info("测试_PCI-E x4, x8 结束！")
            time.sleep(1)

        # 09 总结测试全过程。
            # 01-1
            print("===============================")
            logging.info("===============================")
            print("===============================")
            logging.info("===============================")
            print("===============================")
            logging.info("===============================")
            print("===============================")
            logging.info("===============================")
            if enp12_mac_verify == True:
                print('01-1_MAC address of enp12 is Passed! ')
                logging.info("01-1_MAC address of enp12 is Passed! ")
            else:
                print('01-1_MAC address of enp12 is error!')
                logging.info("01-1_MAC address of enp12 is error!")

            # 01-2
            if enp11_mac_verify == True:
                print('01-2_MAC address of enp11 is Passed! ')
                logging.info("01-2_MAC address of enp11 is Passed! ")
            else:
                print('01-2_MAC address of enp11 is error!')
                logging.info("01-2_MAC address of enp11 is error!")

            # 01-3
            if enp3_mac_verify == True:
                print('01-3_MAC address of enp3 is Passed! ')
                logging.info("01-3_MAC address of enp3 is Passed!")
            else:
                print('01-3_MAC address of enp3 is error!')
                logging.info("01-3_MAC address of enp3 is error!")

            # 02-1
            if enp12s0f2_eth_result == True:
                print('02-1_enp12s0f2_eth_result is Passed! ')
                logging.info("02-1_enp12s0f2_eth_result is Passed!")
            else:
                print('02-1_enp12s0f2_eth_result is error!')
                logging.info("02-1_enp12s0f2_eth_result is error!")

            # 02-2
            if enp12s0f3_eth_result == True:
                print('02-2_enp12s0f3_eth_result is Passed! ')
                logging.info("02-2_enp12s0f3_eth_result is Passed!")
            else:
                print('02-2_enp12s0f3_eth_result is error!')
                logging.info("02-2_enp12s0f3_eth_result is error!")

            # 02-3
            if enp11s0f1_eth_result == True:
                print('02-3_enp11s0f1_eth_result is Passed! ')
                logging.info("02-3_enp11s0f1_eth_result is Passed!")
            else:
                print('02-3_enp11s0f1_eth_result is error!')
                logging.info("02-3_enp11s0f1_eth_result is error!")

            # 02-4
            if enp11s0f0_eth_result == True:
                print('02-4_enp11s0f0_eth_result is Passed! ')
                logging.info("02-4_enp11s0f0_eth_result is Passed!")
            else:
                print('02-4_enp11s0f0_eth_result is error!')
                logging.info("02-4_enp11s0f0_eth_result is error!")

            # 02-5
            if enp3s0f3_eth_result == True:
                print('02-5_enp3s0f3_eth_result is Passed! ')
                logging.info("02-5_enp3s0f3_eth_result is Passed!")
            else:
                print('02-5_enp3s0f3_eth_result is error!')
                logging.info("02-5_enp3s0f3_eth_result is error!")

            # 03
            if bios_result == True:
                print('03-bios_result is Passed! ')
                logging.info("03-bios_result is Passed!")
            else:
                print('03-bios_result is error!')
                logging.info("03-bios_result is error!")

            # 04
            if cpu_result == True:
                print('04-cpu_result is Passed! ')
                logging.info("04-cpu_result is Passed!")
            else:
                print('04-cpu_result is error!')
                logging.info("04-cpu_result is error!")

            # 05
            if memory_result == True:
                print('05-memory_result is Passed! ')
                logging.info("05-memory_result is Passed!")
            else:
                print('05-memory_result is error!')
                logging.info("05-memory_result is error!")

            # 06
            if sn_verify == True:
                print('06-sn_verify is Passed! ')
                logging.info("06-sn_verify is Passed! ")
            else:
                print('06-sn_verify is error!')
                logging.info("06-sn_verify is error!")

            # 07
            if disk_usb_result == True:
                print('07-disk_usb_result is Passed! ')
                logging.info("07-disk_usb_result is Passed! ")
            else:
                print('07-disk_usb_result is error!')
                logging.info("07-disk_usb_result is error!")

            # 08
            if pci_e_x4_x8_result == True:
                print('08-pci_e_x4_x8_result is Passed! ')
                logging.info("08-pci_e_x4_x8_result is Passed! ")
            else:
                print('08-pci_e_x4_x8_result is error!')
                logging.info("08-pci_e_x4_x8_result is error!")


            print("结束：第9次启动： 通过SSH进入操作系统,测试Spinel ")
            logging.info("结束：第9次启动： 通过SSH进入操作系统,测试Spinel ")

        # 程序结束，处理时间以及log文件。
            t2 = time.time()
            print(t2-t1)
            print("Test completely!")

            total_result1 = enp12_mac_verify and enp11_mac_verify and enp3_mac_verify
            total_result2 = enp12s0f2_eth_result and enp12s0f3_eth_result and enp11s0f1_eth_result and enp11s0f0_eth_result and enp3s0f3_eth_result
            total_result3 = bios_result and cpu_result and memory_result and sn_verify and disk_usb_result and pci_e_x4_x8_result

            total_result = total_result1 and total_result2 and total_result3

            if total_result == True:
                logging.info(':Successfully!')
                print("Successfully!")

                t2 = time.time()
                duration = t2 - t1
                logging.critical(': test duration:_' + str(duration))
                print(duration)

                # 处理log 文件， deal with log file in system
                test_time = datetime.now()
                test_time1 = test_time.strftime("%c")
                test_time2 = test_time1.replace(':', '-')
                logging.shutdown()
                os.rename(r'C:\Users\Zhen Wang\Desktop\0211_test_log\20212021.log',
                          r'C:\Users\Zhen Wang\Desktop\0211_test_log\SN_{}.log'.format(
                              spinel_sn + '_' + test_time2 + '_' + 'Passed'))

                # 发送邮件开始
                smtp_server = 'smtp.sina.com'
                port = 465
                sender = 'yuchen556@sina.com'
                # password = input('Enter your password here: ')
                receiver = "556wangzhen@163.com"
                # receiver = 'zhen.wang@joinus-tech.com'
                message = "Subject: Passed_Spinel_Test_{}!\r\nThis message was sent from Python!\r\nFrom: {}\r\nTo: {}".format(spinel_sn, sender, receiver)

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender, 'cd443ab65c8e8431')
                    print("Passed, mailed!")
                    server.sendmail(sender, receiver, message)
                # 发送邮件结束



            else:
                logging.info('Spinel test is Error!')
                print("Spinel test is Error!")

                t2 = time.time()
                duration = t2 - t1
                logging.critical(': test duration:_' + str(duration))
                print(duration)

                # 处理log 文件， deal with log file in system
                test_time = datetime.now()
                test_time1 = test_time.strftime("%c")
                test_time2 = test_time1.replace(':', '-')
                logging.shutdown()
                os.rename(r'C:\Users\Zhen Wang\Desktop\0211_test_log\20212021.log',
                          r'C:\Users\Zhen Wang\Desktop\0211_test_log\SN_{}.log'.format(
                              spinel_sn + '_' + test_time2 + '_' + 'Failed!!!!!!!!!!'))

                # 发送邮件开始
                smtp_server = 'smtp.sina.com'
                port = 465
                sender = 'yuchen556@sina.com'
                # password = input('Enter your password here: ')
                receiver = "556wangzhen@163.com"
                # receiver = 'zhen.wang@joinus-tech.com'
                message = "Subject: Failed_Spinel_Test_{}!\r\nThis message was sent from Python!\r\nFrom: {}\r\nTo: {}".format(spinel_sn, sender, receiver)

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender, 'cd443ab65c8e8431')
                    print("Failed, mailed!")
                    server.sendmail(sender, receiver, message)
                # 发送邮件结束

            quit()

        # 若sn 不是13位的，则提示sn is incorrect；
        else:
            label3 = tk.Label(root, text='SN is incorrect', fg='red', font=('helvetica', 10,))
            canvas1.create_window(200, 210, window=label3)

            label4 = tk.Label(root, text=spinel_sn, font=('helvetica', 10, 'bold'))
            canvas1.create_window(200, 230, window=label4)

            button1.configure(background="black")


    # 点击button，运行get_spinel_sn() 函数:
    button1 = tk.Button(text='Testing', command=get_spinel_sn, bg='brown', fg='white', font=('helvetica', 18, 'bold'))
    canvas1.create_window(540, 500, window=button1)

    root.mainloop()

else:
    # 调用图形界面
    root = tk.Tk()
    # 图形界面的大小 400*300
    canvas1 = tk.Canvas(root, width=1080, height=720, relief='raised')
    canvas1.pack()
    # 图形界面里显示的文字、及位置
    label1 = tk.Label(root, text='Spinel Test Platform')
    label1.config(font=('helvetica', 35))
    canvas1.create_window(540, 100, window=label1)

    # 图形界面里显示的文字、及位置
    label2 = tk.Label(root, text='Could not test.\r\n Available MAC address is <10.\r\n Please contact SH-Joinus to import more MAC address.')
    label2.config(font=('helvetica', 25))
    canvas1.create_window(540, 500, window=label2)


    root.mainloop()