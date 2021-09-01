import Keyboard_Function
import time
# 将12位的MAC 地址，转换成12个键，使用模拟器发送给Spinel

def One_MAC_TO_12Keys(Mac_string):

    try:
        Temp_MAC=Mac_string.lower()
        for x in Temp_MAC:
            time.sleep(1)
            Keyboard_Function.Keyboard_send(x)
            print(x)

    except Error as error:
        print(error)
    finally:
        print("ENDing_Fetched the row number:")