# 使用这个文件，将字符、数字通过键盘模拟器发送给Spinel
# 键盘模拟器，在电脑上的com port 应该是com 6.
#
import serial
import time
import Camera_Spinel
s = serial.Serial('COM6', 9600)

Sim_Key_dict = {
    "Release_Key": b'\x57\xAB\x00\x02\x08\x00\x00\x00\x00\x00\x00\x00\x00\x0C',
    "Send_Up_Arrow": b'\x57\xAB\x00\x02\x08\x00\x00\x52\x00\x00\x00\x00\x00\x5E',
    "Send_Down_Arrow": b'\x57\xAB\x00\x02\x08\x00\x00\x51\x00\x00\x00\x00\x00\x5D',
    "Send_Left_Arrow": b'\x57\xAB\x00\x02\x08\x00\x00\x50\x00\x00\x00\x00\x00\x5C',
    "Send_Right_Arrow": b'\x57\xAB\x00\x02\x08\x00\x00\x4F\x00\x00\x00\x00\x00\x5B',

    "Send_Enter": b'\x57\xAB\x00\x02\x08\x00\x00\x28\x00\x00\x00\x00\x00\x34',
    "Send_Exclamation_mark": b'\x57\xAB\x00\x02\x08\x02\x00\x1E\x00\x00\x00\x00\x00\x2C',
    "Send_F1": b'\x57\xAB\x00\x02\x08\x00\x00\x3A\x00\x00\x00\x00\x00\x46',
    "Send_F10": b'\x57\xAB\x00\x02\x08\x00\x00\x43\x00\x00\x00\x00\x00\x4F',
    "Serial_feadback": b'W\xab\x00\x82\x01\x00\x85',


    # 2月10日更新
    "Send_tab": b'\x57\xAB\x00\x02\x08\x00\x00\x2B\x00\x00\x00\x00\x00\x37',
    "Send_space": b'\x57\xAB\x00\x02\x08\x00\x00\x2C\x00\x00\x00\x00\x00\x38',
    "Send-": b'\x57\xAB\x00\x02\x08\x00\x00\x2D\x00\x00\x00\x00\x00\x39',
    "Send_": b'\x57\xAB\x00\x02\x08\x02\x00\x2D\x00\x00\x00\x00\x00\x3B',

    "Send_dot": b'\x57\xAB\x00\x02\x08\x00\x00\x37\x00\x00\x00\x00\x00\x43',
    "Send/": b'\x57\xAB\x00\x02\x08\x00\x00\x38\x00\x00\x00\x00\x00\x44',

    "Send_F": b'\x57\xAB\x00\x02\x08\x02\x00\x09\x00\x00\x00\x00\x00\x17',
    "Send_P": b'\x57\xAB\x00\x02\x08\x02\x00\x13\x00\x00\x00\x00\x00\x21',
    "Send_U": b'\x57\xAB\x00\x02\x08\x02\x00\x18\x00\x00\x00\x00\x00\x26',


    # 1月20日更新：
    "Send_a": b'\x57\xAB\x00\x02\x08\x00\x00\x04\x00\x00\x00\x00\x00\x10',
    "Send_b": b'\x57\xAB\x00\x02\x08\x00\x00\x05\x00\x00\x00\x00\x00\x11',
    "Send_c": b'\x57\xAB\x00\x02\x08\x00\x00\x06\x00\x00\x00\x00\x00\x12',
    "Send_d": b'\x57\xAB\x00\x02\x08\x00\x00\x07\x00\x00\x00\x00\x00\x13',
    "Send_e": b'\x57\xAB\x00\x02\x08\x00\x00\x08\x00\x00\x00\x00\x00\x14',
    "Send_f": b'\x57\xAB\x00\x02\x08\x00\x00\x09\x00\x00\x00\x00\x00\x15',
    "Send_g": b'\x57\xAB\x00\x02\x08\x00\x00\x0A\x00\x00\x00\x00\x00\x16',
    "Send_h": b'\x57\xAB\x00\x02\x08\x00\x00\x0B\x00\x00\x00\x00\x00\x17',
    "Send_i": b'\x57\xAB\x00\x02\x08\x00\x00\x0C\x00\x00\x00\x00\x00\x18',
    "Send_j": b'\x57\xAB\x00\x02\x08\x00\x00\x0D\x00\x00\x00\x00\x00\x19',
    "Send_k": b'\x57\xAB\x00\x02\x08\x00\x00\x0E\x00\x00\x00\x00\x00\x1A',
    "Send_l": b'\x57\xAB\x00\x02\x08\x00\x00\x0F\x00\x00\x00\x00\x00\x1B',
    "Send_m": b'\x57\xAB\x00\x02\x08\x00\x00\x10\x00\x00\x00\x00\x00\x1C',
    "Send_n": b'\x57\xAB\x00\x02\x08\x00\x00\x11\x00\x00\x00\x00\x00\x1D',
    "Send_o": b'\x57\xAB\x00\x02\x08\x00\x00\x12\x00\x00\x00\x00\x00\x1E',
    "Send_p": b'\x57\xAB\x00\x02\x08\x00\x00\x13\x00\x00\x00\x00\x00\x1F',
    "Send_q": b'\x57\xAB\x00\x02\x08\x00\x00\x14\x00\x00\x00\x00\x00\x20',
    "Send_r": b'\x57\xAB\x00\x02\x08\x00\x00\x15\x00\x00\x00\x00\x00\x21',
    "Send_s": b'\x57\xAB\x00\x02\x08\x00\x00\x16\x00\x00\x00\x00\x00\x22',
    "Send_t": b'\x57\xAB\x00\x02\x08\x00\x00\x17\x00\x00\x00\x00\x00\x23',
    "Send_u": b'\x57\xAB\x00\x02\x08\x00\x00\x18\x00\x00\x00\x00\x00\x24',
    "Send_v": b'\x57\xAB\x00\x02\x08\x00\x00\x19\x00\x00\x00\x00\x00\x25',
    "Send_w": b'\x57\xAB\x00\x02\x08\x00\x00\x1A\x00\x00\x00\x00\x00\x26',
    "Send_x": b'\x57\xAB\x00\x02\x08\x00\x00\x1B\x00\x00\x00\x00\x00\x27',
    "Send_y": b'\x57\xAB\x00\x02\x08\x00\x00\x1C\x00\x00\x00\x00\x00\x28',
    "Send_z": b'\x57\xAB\x00\x02\x08\x00\x00\x1D\x00\x00\x00\x00\x00\x29',
    "Send_1": b'\x57\xAB\x00\x02\x08\x00\x00\x1E\x00\x00\x00\x00\x00\x2A',
    "Send_2": b'\x57\xAB\x00\x02\x08\x00\x00\x1F\x00\x00\x00\x00\x00\x2B',
    "Send_3": b'\x57\xAB\x00\x02\x08\x00\x00\x20\x00\x00\x00\x00\x00\x2C',
    "Send_4": b'\x57\xAB\x00\x02\x08\x00\x00\x21\x00\x00\x00\x00\x00\x2D',
    "Send_5": b'\x57\xAB\x00\x02\x08\x00\x00\x22\x00\x00\x00\x00\x00\x2E',
    "Send_6": b'\x57\xAB\x00\x02\x08\x00\x00\x23\x00\x00\x00\x00\x00\x2F',
    "Send_7": b'\x57\xAB\x00\x02\x08\x00\x00\x24\x00\x00\x00\x00\x00\x30',
    "Send_8": b'\x57\xAB\x00\x02\x08\x00\x00\x25\x00\x00\x00\x00\x00\x31',
    "Send_9": b'\x57\xAB\x00\x02\x08\x00\x00\x26\x00\x00\x00\x00\x00\x32',
    "Send_0": b'\x57\xAB\x00\x02\x08\x00\x00\x27\x00\x00\x00\x00\x00\x33',
}


# 键盘大全
def Keyboard_send(soft_key):
    # a->z
    if soft_key == "a":
        s.write(Sim_Key_dict["Send_a"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "b":
        s.write(Sim_Key_dict["Send_b"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "c":
        s.write(Sim_Key_dict["Send_c"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "d":
        s.write(Sim_Key_dict["Send_d"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "e":
        s.write(Sim_Key_dict["Send_e"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "f":
        s.write(Sim_Key_dict["Send_f"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "g":
        s.write(Sim_Key_dict["Send_g"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "h":
        s.write(Sim_Key_dict["Send_h"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "i":
        s.write(Sim_Key_dict["Send_i"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "j":
        s.write(Sim_Key_dict["Send_j"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "k":
        s.write(Sim_Key_dict["Send_k"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "l":
        s.write(Sim_Key_dict["Send_l"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "m":
        s.write(Sim_Key_dict["Send_m"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "n":
        s.write(Sim_Key_dict["Send_n"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "o":
        s.write(Sim_Key_dict["Send_o"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "p":
        s.write(Sim_Key_dict["Send_p"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "q":
        s.write(Sim_Key_dict["Send_q"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "r":
        s.write(Sim_Key_dict["Send_r"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "s":
        s.write(Sim_Key_dict["Send_s"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "t":
        s.write(Sim_Key_dict["Send_t"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "u":
        s.write(Sim_Key_dict["Send_u"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "v":
        s.write(Sim_Key_dict["Send_v"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "w":
        s.write(Sim_Key_dict["Send_w"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "x":
        s.write(Sim_Key_dict["Send_x"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "y":
        s.write(Sim_Key_dict["Send_y"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "z":
        s.write(Sim_Key_dict["Send_z"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    # capital 大写字母
    elif soft_key == "F":
        s.write(Sim_Key_dict["Send_F"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "P":
        s.write(Sim_Key_dict["Send_P"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "U":
        s.write(Sim_Key_dict["Send_U"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])

    #############################################
    # 1->9->0
    elif soft_key == "1":
        s.write(Sim_Key_dict["Send_1"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "2":
        s.write(Sim_Key_dict["Send_2"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "3":
        s.write(Sim_Key_dict["Send_3"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "4":
        s.write(Sim_Key_dict["Send_4"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "5":
        s.write(Sim_Key_dict["Send_5"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "6":
        s.write(Sim_Key_dict["Send_6"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "7":
        s.write(Sim_Key_dict["Send_7"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "8":
        s.write(Sim_Key_dict["Send_8"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "9":
        s.write(Sim_Key_dict["Send_9"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "0":
        s.write(Sim_Key_dict["Send_0"])
        time.sleep(0.1)
        s.write(Sim_Key_dict["Release_Key"])
    #############################################
    # Send_Up_Arrow, Send_Down_Arrow, Send_Left_Arrow
    # Send_Right_Arrow, Send_Enter, Send_Exclamation_mark
    # Send_F1, Send_F10, Send_tab, Send_space, Send-, Send_
    # Send_dot, Send/
    #############################################

    elif soft_key == "Send_Up_Arrow":
        s.write(Sim_Key_dict["Send_Up_Arrow"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send_Down_Arrow":
        s.write(Sim_Key_dict["Send_Down_Arrow"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send_Left_Arrow":
        s.write(Sim_Key_dict["Send_Left_Arrow"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send_Right_Arrow":
        s.write(Sim_Key_dict["Send_Right_Arrow"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send_Enter":
        s.write(Sim_Key_dict["Send_Enter"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send_Exclamation_mark":
        s.write(Sim_Key_dict["Send_Exclamation_mark"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send_F1":
        s.write(Sim_Key_dict["Send_F1"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send_F10":
        s.write(Sim_Key_dict["Send_F10"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send_tab":
        s.write(Sim_Key_dict["Send_tab"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send_space":
        s.write(Sim_Key_dict["Send_space"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send-":
        s.write(Sim_Key_dict["Send-"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send_":
        s.write(Sim_Key_dict["Send_"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
        time.sleep(0.01)
    elif soft_key == "Send_dot":
        s.write(Sim_Key_dict["Send_dot"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    elif soft_key == "Send/":
        s.write(Sim_Key_dict["Send/"])
        time.sleep(0.01)
        s.write(Sim_Key_dict["Release_Key"])
    else:
        print("soft_key_error")

# 键盘测试大全
# Keyboard_send("Send_Up_Arrow")
# Keyboard_send("Send_Down_Arrow")
# Keyboard_send("Send_Left_Arrow")
# Keyboard_send("Send_Right_Arrow")
# Keyboard_send("Send_Enter")
# Keyboard_send("Send_Exclamation_mark")
# Keyboard_send("Send_F1")
# Keyboard_send("Send_F10")

# Keyboard_send("a")
# Keyboard_send("b")
# Keyboard_send("c")
# Keyboard_send("d")
# Keyboard_send("e")
# Keyboard_send("f")
# Keyboard_send("g")
# Keyboard_send("h")
# Keyboard_send("i")
# Keyboard_send("j")
# Keyboard_send("k")
# Keyboard_send("l")
# Keyboard_send("m")
# Keyboard_send("n")
# Keyboard_send("o")
# Keyboard_send("p")
# Keyboard_send("q")
# Keyboard_send("r")
# Keyboard_send("s")
# Keyboard_send("t")
# Keyboard_send("u")
# Keyboard_send("v")
# Keyboard_send("w")
# Keyboard_send("x")
# Keyboard_send("y")
# Keyboard_send("z")
#
# Keyboard_send("1")
# Keyboard_send("2")
# Keyboard_send("3")
# Keyboard_send("4")
# Keyboard_send("5")
# Keyboard_send("6")
# Keyboard_send("7")
# Keyboard_send("8")
# Keyboard_send("9")
# Keyboard_send("0")

# time.sleep(1)
# Keyboard_send("c")
# time.sleep(1)
# Keyboard_send("d")
# time.sleep(1)
# Keyboard_send("Send_space")
# time.sleep(1)
# Keyboard_send("s")
# time.sleep(1)
# Keyboard_send("Send_tab")
# time.sleep(1)
# Keyboard_send("Send_Enter")
# time.sleep(1)
# # Keyboard_send("Send/")
# time.sleep(1)
# Keyboard_send("Send_dot")
# time.sleep(1)
# Keyboard_send("Send-")
# time.sleep(1)
# Keyboard_send("Send_")
# time.sleep(1)


# F1 按键
def bios_f1():
    for num in range(1, 60):
        Keyboard_send("Send_F1")
        time.sleep(1)


# secadm 用户名
def secadm_usr():
    # =====================================
    time.sleep(1)
    Keyboard_send("s")
    time.sleep(2)

    # =====================================
    Keyboard_send("e")
    time.sleep(2)

    # =====================================
    Keyboard_send("c")
    time.sleep(2)

    # =====================================
    Keyboard_send("a")
    time.sleep(2)

    # =====================================
    Keyboard_send("d")
    time.sleep(2)

    # =====================================
    Keyboard_send("m")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(3)


# secadm 密码
def secadm_pw():
    # 发送15个a ============================
    time.sleep(1)
    count_1 = 1
    while count_1 < 16:
        Keyboard_send("a")
        time.sleep(1)
        count_1 = count_1 + 1

    # 发送1个1 ==============================
    time.sleep(2)
    Keyboard_send("1")
    time.sleep(3)

    # 发送1个感叹号 =========================
    Keyboard_send("Send_Exclamation_mark")
    time.sleep(3)

    # 发送回车 ==============================
    Keyboard_send("Send_Enter")
    time.sleep(10)


# root 用户名
def root_usr():
    # =====================================
    time.sleep(2)
    Keyboard_send("r")
    time.sleep(2)

    # =====================================
    Keyboard_send("o")
    time.sleep(2)

    # =====================================
    Keyboard_send("o")
    time.sleep(2)

    # =====================================
    Keyboard_send("t")
    time.sleep(2)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(3)


# root 密码
def root_pw():
    # 发送15个1 ============================
    time.sleep(1)
    count_1 = 1
    while count_1 < 16:
        Keyboard_send("1")
        time.sleep(1)
        count_1 = count_1 + 1

    # 发送1个1 ==============================
    time.sleep(2)
    Keyboard_send("a")
    time.sleep(3)

    # 发送1个感叹号 =========================
    Keyboard_send("Send_Exclamation_mark")
    time.sleep(3)

    # 发送回车 ==============================
    Keyboard_send("Send_Enter")
    time.sleep(20)


# 02-硬盘加密关闭
def Close_HDD_security():
    # Step01: right, enter, sleep 15s

    # =====================================
    time.sleep(20)
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

    # Step02: right, right, down,enter
    # =====================================
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

# Step03: enter, up, enter, enter
    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Up_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)


# 03-启动项管理开关，打开
def Open_boot_item():
    # Step01: right, enter, sleep 15s

    # =====================================
    time.sleep(20)
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

 # Step02: right, right, down, down, enter
    # =====================================
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

# Step03: down, enter, down, enter
    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

# Step04: F10, enter
    # =====================================
    Keyboard_send("Send_F10")
    time.sleep(15)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)


# 04-安全-> 可信计算配置 -> 更新所有的预期值
def update_safety_setting():
# Step01: right, enter, sleep 15s

    # =====================================
    time.sleep(20)
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

# Step02: right, right, down, down, down, enter
    # =====================================
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

# Step03: down, down, down, down, down, enter
    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Down_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

# Step04:  enter
    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)


# 05-设置U盘启动
def pre_usb_key_action():
    # Step01: right, enter, sleep 15s

    # =====================================
    time.sleep(20)
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

    # Step02: right, right, right,enter
    # =====================================
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)


def USB_Boot(USB_Disk_check, device_quantity):

    # Step03: chose USB disk
    time.sleep(2)
    print(device_quantity)
    print(USB_Disk_check)
    if device_quantity == 7:
        if USB_Disk_check == 1:
            # =====================================
            Keyboard_send("Send_Enter")
            print("U disk is at 1st row")
            time.sleep(15)
            sandisk = True
        elif USB_Disk_check == 2:
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)

            # =====================================
            Keyboard_send("Send_Enter")
            print("U disk is at 2ed row")
            time.sleep(15)
            sandisk = True
        elif USB_Disk_check == 3:
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Enter")
            print("U disk is at 3rd row")
            time.sleep(15)
            sandisk = True
        elif USB_Disk_check == 4:
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Enter")
            print("U disk is at 4th row")
            time.sleep(15)
            sandisk = True
        elif USB_Disk_check == 5:
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Enter")
            print("U disk is at 5th row")
            time.sleep(15)
            sandisk = True
        elif USB_Disk_check == 6:
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Enter")
            print("U disk is at 6th row")
            time.sleep(15)
            sandisk = True
        elif USB_Disk_check == 7:
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Down_Arrow")
            time.sleep(3)
            # =====================================
            Keyboard_send("Send_Enter")
            print("U disk is at 7th row")
            time.sleep(15)
            sandisk = True
    else:
        print("Error: the USB disk is not correct")
        sandisk = False



    # Step04: F10, enter
    # =====================================
    Keyboard_send("Send_F10")
    time.sleep(15)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)
    return sandisk


# 06-Centos 用户名+密码
def centos_user_pw():
    # Step01: right, enter, sleep 15s
    # 用于不更改密码
    # =====================================
    time.sleep(12)
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)


    # =====================================
    Keyboard_send("Send_Enter")


    # Step02: enter
    # =====================================
    time.sleep(3)
    Keyboard_send("Send_Enter")
    time.sleep(40)


   # Step03: "root", enter
    # =====================================
    time.sleep(1)
    Keyboard_send("r")
    time.sleep(1)


    # =====================================
    Keyboard_send("o")
    time.sleep(1)

    # =====================================
    Keyboard_send("o")
    time.sleep(1)

    # =====================================
    Keyboard_send("t")
    time.sleep(1)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)

    # Step04: "1", enter
    # =====================================
    time.sleep(1)
    Keyboard_send("1")
    time.sleep(1)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(15)


# 07-输入完root用户名和密码后的，right and enter
def keyboard_right_enter_to_centos():
    # Step01: right, enter, sleep 15s

    # =====================================
    time.sleep(20)
    Keyboard_send("Send_Right_Arrow")
    time.sleep(3)

    # =====================================
    Keyboard_send("Send_Enter")
    time.sleep(70)


# keyboard_right_enter_to_centos()
