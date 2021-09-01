import mysql.connector
# 找到10个MAC 地址，将这10个 MAC address 返回给一个列表

def MAC_adds_TO_Array(add_to_array):

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="mac_status")
        mycursor = mydb.cursor()
        tmp_list = []
        for x in range(add_to_array, add_to_array+10):
            query0 = "SELECT * FROM mac_spinel WHERE id = {0:d} ".format(x)
            mycursor.execute(query0)
            MAC_result = mycursor.fetchone()
            # 下面的命令是将MAC 追加到列表里。
            tmp_list.append(MAC_result[1])
            # print(MAC_result[1])
            # print(type(MAC_result[1]))
        return tmp_list

    except Error as error:
        print(error)
    finally:
        # mycursor.close()
        # mydb.close()
        print("ENDing_Fetched the row number:")
