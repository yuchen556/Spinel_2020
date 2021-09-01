# 使用ssh 建立Pycharm 与 CentOS 的链接；
# 连接在Spinel上的USB_转_USB+网口，的IP address： 192.168.1.153；
#
#

import paramiko
import time
import numpy as np
import re

# 下面函数通过SSH 建立与spinel的链接，并返回channel and ssh_client。
def connect_spinel_ssh():
    """ Connect to a device, run a command, and return the output."""

    spinel_ip = "192.168.1.153"
    spinel_port = 22
    spinel_username = "root"
    spinel_password = "1"

    # 创建一个SSH客户端client对象
    ssh_spinel = paramiko.SSHClient()
    ssh_spinel.load_system_host_keys()

    # Add SSH host key when missing.
    # 这个代码指的是将目标主机的信息添加至know_hosts文件中，know_hosts文件在当前用户下的 .
    # ssh文件夹下，是一个隐藏文件，当你第一次使用ssh 用户+@+ip的方式远程登录另一台机器时，
    # 系统也会提示你是否将目标机器的信息添加至know_hosts文件中。
    ssh_spinel.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    total_attempts = 3

    for attempt in range(total_attempts):
        try:
            print("SSH_Attempt_to_connect: %s" % attempt)
            # connect方法实现了远程SSH连接并校验
            ssh_spinel.connect(spinel_ip, port=spinel_port, username=spinel_username, password=spinel_password, look_for_keys=False)

            # 通过Client 建立一个通道;
            # open_session(window_size=None, max_packet_size=None, timeout=None)¶
            # Request a new channel to the server, of type "session".
            # This is just an alias for calling open_channel with an argument of "session".
            # Parameters:
            # window_size (int) – optional window size for this session.
            # max_packet_size (int) – optional max packet size for this session.
            # Returns:	a new Channel
            #
            # Raises: SSHException – if the request is rejected or the session ends prematurely
            channel1 = ssh_spinel.get_transport().open_session()

            # get_pty(term='vt100', width=80, height=24, width_pixels=0, height_pixels=0)
            # Request a pseudo-terminal from the server.
            # This is usually used right after creating a client channel,
            # to ask the server to provide some basic terminal semantics
            # for a shell invoked with invoke_shell.
            # It isn’t necessary (or desirable) to call this method
            # if you’re going to execute a single command with exec_command.

            channel1.get_pty()

            # 需要分清楚，client 里的invoke_shell 与 Channel 里的invoke_shell 有什么不一样！！
            # 这个函数的作用是启动起来一个 shell 窗口。虽然看不到什么，但目的是启动一个shell。
            channel1.invoke_shell()

            print("%s time connected via SSH. " % attempt)

            return channel1, ssh_spinel

        except Exception as error_message:
            print("Unable to connect via SSH!")
            print(error_message)


# 此函数via SSH 发送命令给spinel
def send_command_to_spinel_ssh(command1, channel_spinel):
    channel_spinel.send(command1 + "\n")
    while True:
        if channel_spinel.recv_ready():
            output = channel_spinel.recv(65534)
            # decode("utf-8") 将bytes 转换成 string
            ttt1 = output.decode("utf-8")
            print(ttt1)
            return ttt1
        else:
            time.sleep(0.5)
            if not (channel_spinel.recv_ready()):
                break

    time.sleep(2)


# 此函数关闭ssh_channel 和 ssh_client
def disconnect_ssh(spinel_ssh_channel, spinel_ssh_client):
    spinel_ssh_channel.close()
    spinel_ssh_client.close()

# 获取到ssh channel 和 ssh client
# channel_spinel, ssh_client_spinel = connect_spinel_ssh()

# 更新MAC 地址
def update_enp12s0f0_mac(MAC_for_enp12, PC_SN, internal_channel):
    command = 'cd /root/spinel'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    command = './wangxun_upgrade_tool_x86_for_cu -F SF400HF_30010013.img -U'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 选择1000M 网卡
    command = '1'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 选择 enp12s0f0 网卡
    command = '0'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 输入第一个MAC地址
    command = MAC_for_enp12
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 输入整机序列号
    command = PC_SN
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 系统更新eeprom 需要120s
    time.sleep(120)

# 更新MAC 地址
def update_enp11s0f0_mac(MAC_for_enp11, PC_SN, internal_channel):
    command = 'cd /root/spinel'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    command = './wangxun_upgrade_tool_x86_for_cu -F SF200HT_10008.img -U -P'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 选择1000M 网卡
    command = '1'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 选择 enp11s0f0 网卡
    command = '1'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 输入第一个MAC地址
    command = MAC_for_enp11
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 输入整机序列号
    command = PC_SN
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 系统更新eeprom 需要120s
    time.sleep(120)

# 更新MAC 地址
def update_enp3s0f0_mac(MAC_for_enp3, PC_SN, internal_channel):
    command = 'cd /root/spinel'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    command = './wangxun_upgrade_tool_x86_for_cu -F SF400HT_10008.img -U'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 选择1000M 网卡
    command = '1'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 选择 enp3s0f0 网卡
    command = '2'
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 输入第一个MAC地址
    command = MAC_for_enp3
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 输入整机序列号
    command = PC_SN
    send_command_to_spinel_ssh(command, internal_channel)
    time.sleep(2)

    # 系统更新eeprom 需要120s
    time.sleep(120)


# 测试MAC 地址
def t_01_enp12s0f0_mac_verify(internal_channel, MAC_0, MAC_1, MAC_2, MAC_3):
    command = 'cd /root/spinel'
    send_command_to_spinel_ssh(command, internal_channel)

    command = './wangxun_upgrade_tool_x86_for_cu -F SF400HF_30010013.img -U'
    send_command_to_spinel_ssh(command, internal_channel)

    # 选择1000M 网卡
    command = '1'
    send_command_to_spinel_ssh(command, internal_channel)

    # 选择 enp12s0f0 网卡
    command = '0'
    print("1------------start---------------")
    enp12_MAC_and_SN = send_command_to_spinel_ssh(command, internal_channel)

    print("2------------start---------------")
    string4 = enp12_MAC_and_SN.split()
    if (MAC_0.lower() == string4[19][2:]) and (MAC_1.lower() == string4[23][2:]) and (MAC_2.lower() == string4[27][2:])and (MAC_3.lower() == string4[31][2:]):
        print(string4[19][2:])
        print(string4[23][2:])
        print(string4[27][2:])
        print(string4[31][2:])
        enp12_MAC_address_correct = True
        return enp12_MAC_address_correct
    else:
        print("Error: incorrect of MAC enp12s0f0!")
        enp12_MAC_address_correct = False
        return enp12_MAC_address_correct

    # print(x)

# 测试MAC 地址
def t_01_enp11s0f0_mac_verify(internal_channel, MAC_4, MAC_5):
    command = 'cd /root/spinel'
    send_command_to_spinel_ssh(command, internal_channel)

    command = './wangxun_upgrade_tool_x86_for_cu -F SF200HT_10008.img -U -P'
    send_command_to_spinel_ssh(command, internal_channel)

    # 选择1000M 网卡
    command = '1'
    send_command_to_spinel_ssh(command, internal_channel)

    # 选择 enp11s0f0 网卡
    command = '1'
    enp11_MAC_and_SN = send_command_to_spinel_ssh(command, internal_channel)


    print("2------------start---------------")
    string4 = enp11_MAC_and_SN.split()
    # print(string4)
    if (MAC_4.lower() == string4[19][2:]) and (MAC_5.lower() == string4[23][2:]):
        print(string4[19][2:])
        print(string4[23][2:])
        enp11_MAC_address_correct = True
        return  enp11_MAC_address_correct
    else:
        print("Error: incorrect of MAC enp11s0f0!")
        enp11_MAC_address_correct = False
        return enp11_MAC_address_correct

    # print(x)

# 测试MAC 地址
def t_01_enp3s0f0_mac_verify(internal_channel, MAC_6, MAC_7, MAC_8, MAC_9):
    command = 'cd /root/spinel'
    send_command_to_spinel_ssh(command, internal_channel)

    command = './wangxun_upgrade_tool_x86_for_cu -F SF400HT_10008.img -U'
    send_command_to_spinel_ssh(command, internal_channel)

    # 选择1000M 网卡
    command = '1'
    send_command_to_spinel_ssh(command, internal_channel)

    # 选择 enp3s0f0 网卡
    command = '2'
    print("1------------start---------------")
    enp3_MAC_and_SN = send_command_to_spinel_ssh(command, internal_channel)

    print("2------------start---------------")
    string4 = enp3_MAC_and_SN.split()
    if (MAC_6.lower() == string4[19][2:]) and (MAC_7.lower() == string4[23][2:]) and (MAC_8.lower() == string4[27][2:])and (MAC_9.lower() == string4[31][2:]):
        print(string4[19][2:])
        print(string4[23][2:])
        print(string4[27][2:])
        print(string4[31][2:])
        enp3_MAC_address_correct = True
        return  enp3_MAC_address_correct
    else:
        print("Error: incorrect of MAC enp3s0f0!")
        enp3_MAC_address_correct = False
        return enp3_MAC_address_correct

    # print(x)

# 测试网卡，这个函数没有使用
def enp12s0f0_ping_192_168_1_1_(internal_channel):
    command = 'ping -c 2 192.168.1.1'
    result_ping_192_168_1_1 = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_ping_192_168_1_1.split()
    print(string4[32])

    # if (MAC_6.lower() == string4[19][2:]):
    #     print(string4[19][2:])
    #     print(string4[23][2:])
    #     print(string4[27][2:])
    #     print(string4[31][2:])
    #     enp3_MAC_address_correct = True
    #     return  enp3_MAC_address_correct
    # else:
    #     print("Error: incorrect of MAC enp3s0f0!")
    #     enp3_MAC_address_correct = False
    #     return enp3_MAC_address_correct

    # print(x)


# 测试网口
def t_02_1_ethtool_enp12s0f2_(internal_channel):
    command = 'ethtool enp12s0f2'
    result_ethtool_enp12s0f2 = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_ethtool_enp12s0f2.split()

    list_value = string4.index('detected:')

    print(list_value)

    enp12s0f2_result = 'ethtool_enp12s0f2' + ' ' + string4[list_value-1] + ' ' + string4[list_value] + ' ' + string4[list_value+1]
    print(enp12s0f2_result)

    if string4[list_value+1] == "yes":
        print("enp12s0f2 is fine!")
        return True
    else:
        print("enp12s0f2 is error!")
        return False


def t_02_2_ethtool_enp12s0f3_(internal_channel):
    command = 'ethtool enp12s0f3'
    result_ethtool_enp12s0f3 = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_ethtool_enp12s0f3.split()

    list_value = string4.index('detected:')

    print(list_value)

    enp12s0f3_result = 'ethtool_enp12s0f3' + ' ' + string4[list_value-1] + ' ' + string4[list_value] + ' ' + string4[list_value+1]
    print(enp12s0f3_result)

    if string4[list_value + 1] == "yes":
        print("enp12s0f3 is fine!")
        return True
    else:
        print("enp12s0f3 is error!")
        return False


def t_02_3_ethtool_enp11s0f1_(internal_channel):
    command = 'ethtool enp11s0f1'
    result_ethtool_enp11s0f1 = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_ethtool_enp11s0f1.split()

    list_value = string4.index('detected:')

    print(list_value)

    enp11s0f1_result = 'ethtool_enp11s0f1' + ' ' + string4[list_value-1] + ' ' + string4[list_value] + ' ' + string4[list_value+1]
    print(enp11s0f1_result)

    if string4[list_value + 1] == "yes":
        print("enp11s0f1 is fine!")
        return True
    else:
        print("enp11s0f1 is error!")
        return False


def t_02_4_ethtool_enp11s0f0_(internal_channel):
    command = 'ethtool enp11s0f0'
    result_ethtool_enp11s0f0 = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_ethtool_enp11s0f0.split()

    list_value = string4.index('detected:')

    print(list_value)

    enp11s0f0_result = 'ethtool_enp11s0f0' + ' ' + string4[list_value-1] + ' ' + string4[list_value] + ' ' + string4[list_value+1]
    print(enp11s0f0_result)

    if string4[list_value + 1] == "yes":
        print("enp11s0f0 is fine!")
        return True
    else:
        print("enp11s0f0 is error!")
        return False


def t_02_5_ethtool_enp3s0f3_(internal_channel):
    command = 'ethtool enp3s0f3'
    result_ethtool_enp3s0f3 = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_ethtool_enp3s0f3.split()

    list_value = string4.index('detected:')

    print(list_value)

    enp3s0f3_result = 'ethtool_enp3s0f3' + ' ' + string4[list_value-1] + ' ' + string4[list_value] + ' ' + string4[list_value+1]
    print(enp3s0f3_result)

    if string4[list_value + 1] == "yes":
        print("enp3s0f3 is fine!")
        return True
    else:
        print("enp3s0f3 is error!")
        return False


# 测试BIOS version 是否是：BA.1.006.201202
def t_03_check_BIOS_(internal_channel):
    command = 'dmidecode -t 0'
    result_BIOS = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_BIOS.split()

    list_value = string4.index('Version:')

    print(list_value)

    BIOS_result = 'check_BIOS_' + ' ' + string4[list_value] + ' ' + string4[list_value+1]

    print(BIOS_result)
    if string4[list_value + 1] == "BA.1.006.201202":
        print("Passed: BIOS version {} is fine!".format(string4[list_value+1]))
        return True
    else:
        print("Error: BIOS version {} is error!".format(string4[list_value+1]))
        return False


# 测试CP型号是否是：KH-S20000@1.8GHz
def t_04_check_cpu_(internal_channel):
    command = 'lscpu'
    result_cpu = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_cpu.split()
    list_value = string4.index('KH-S20000@1.8GHz')

    print(list_value)
    cpu_result = 'cpu_result_:' + string4[list_value]
    print(cpu_result)
    if string4[list_value] == "KH-S20000@1.8GHz":
        print("Passed: cpu is {} fine!".format(string4[list_value]))
        return True
    else:
        print("Error: cpu is {} error!".format(string4[list_value+1]))
        return False


# 测试4个内存是否都插上
def t_05_check_memory_(internal_channel):
    command = 'free'
    result_cpu = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_cpu.split()

    print("Memory total size: " + string4[20])
    if np.uint32(string4[20]) > 32000000:
        print("Passed, memory. 4 memory are instered!")
        return True
    else:
        print("Failed, memory. Please check the 4 memory !")
        return False


# 测试SN
def t_06_check_spinel_sn(internal_channel):
    command = 'cd /root/spinel'
    send_command_to_spinel_ssh(command, internal_channel)

    command = './wangxun_upgrade_tool_x86_for_cu -F SF400HF_30010013.img -U'
    send_command_to_spinel_ssh(command, internal_channel)

    # 选择1000M 网卡
    command = '1'
    send_command_to_spinel_ssh(command, internal_channel)

    # 选择 enp12s0f0 网卡
    command = '0'
    print("1------------start---------------")
    enp12_MAC_and_SN = send_command_to_spinel_ssh(command, internal_channel)

    print("2------------start---------------")
    string4 = enp12_MAC_and_SN.split()
    serial_number = string4[34][7:]

    if (len(serial_number) == 13) and (serial_number.isnumeric()):
        print(serial_number)
        serial_number_result = True
        return serial_number_result, serial_number
    else:
        print("SN is not correct!")
        serial_number_result = False
        return serial_number_result, serial_number


# 测试SATA, M2, CF, P18-USB1, P18-USB2, J18-USB (六个硬盘)
def t_07_disk_usb_port_(internal_channel):
    command = 'lsblk'
    result_usb_port = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_usb_port.split()

    if "sda" in string4:
        print("sda is detected")
        sda = True
    else:
        print("sda is not inserted")
        sda = False

    if "sdb" in string4:
        print("sdb is detected")
        sdb = True
    else:
        print("sdb is not inserted")
        sdb = False

    if "sdc" in string4:
        print("sdc is detected")
        sdc = True
    else:
        print("sdc is not inserted")
        sdc = False

    if "sdd" in string4:
        print("sdd is detected")
        sdd = True
    else:
        print("sdd is not inserted")
        sdd = False

    if "sde" in string4:
        print("sde is detected")
        sde = True
    else:
        print("sde is not inserted")
        sde = False

    if "sdf" in string4:
        print("sdf is detected")
        sdf = True
    else:
        print("sdf is not inserted")
        sdf = False

    usb_result = sda and sdb and sdc and sdd and sde and sdf
    return usb_result


# 测试1个PCI-E*4, 1个PCI-E*8，是否都插上了PCI-E*1 的网卡
def t_08_check_pci_port_(internal_channel):
    command = 'ifconfig -s'
    result_usb_port = send_command_to_spinel_ssh(command, internal_channel)
    string4 = result_usb_port.split()
    list_number = string4.index("enp10s0")
    print(list_number)
    print(string4[list_number])

    if string4[list_number] == "enp10s0":
        print("PCI-E_*_4 is fine!")
        pci_e_4 = True
    else:
        print("PCI-E_*_4 is error!")
        pci_e_4 = False

    list_number1 = string4.index("enp14s0")
    print(list_number1)
    print(string4[list_number1])
    if string4[list_number1] == "enp14s0":
        print("PCI-E_*_8 is fine!")
        pci_e_8 = True
    else:
        print("PCI-E_*_8 is error!")
        pci_e_8 = False

    pci_ports_result = pci_e_4 and pci_e_8
    return pci_ports_result


