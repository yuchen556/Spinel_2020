# 寻找SN 是否在mac_spinel的这个table里，最终返回一个行数。此行数是所需要的第一个MAC地址的行数。
import mysql.connector

# 函数说明：处理扫描枪得到的sn
# 若sn没有在数据库mac_status 的mac_spinel 这个表里，则寻找第一个sn= free的行号；
#     然后将这个sn 写入10行，起始行数是第一个free的行数；
#     写入之后，提取此sn 对应的mac 地址；
# 若sn已经在这个数据库里了，说明已经测试过了。就提取相应的10个MAC地址；

def search_db_sn(inter_sn):
    # query0: search the scanned sn is existed in mac_spinel table or not
    query0 = "SELECT * FROM mac_spinel WHERE sn = '{0:s}'".format(inter_sn)
    # query01: search the free in the mac_spinel table or not
    internal_free = "free"
    query01 = "SELECT * FROM mac_spinel WHERE sn = '{0:s}'".format(internal_free)
    print(inter_sn)
    print(type(inter_sn))

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="mac_status")
        mycursor = mydb.cursor()
        print(query0)

        # get all the rowcount of this sn
        mycursor.execute(query0)
        result_query0_all = mycursor.fetchall()
        print(2, inter_sn, mycursor.rowcount)


        # mycursor.rowcount = 0: if there isn't the sn in mac_spinel table, search the 1st free row ID;
        if mycursor.rowcount == 0:
            print("This SN is new one.")
            print(query01)
            mycursor.execute(query01)
            result_query1_one = mycursor.fetchone()
            result_query1_int = result_query1_one[0]
            # query11: write the sn to free 10 * row
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="mac_status")
            mycursor = mydb.cursor()
            for sn_x0 in range(result_query1_int, result_query1_int+10):
                query11 = " UPDATE mac_spinel SET sn = '{0:s}' WHERE id = {1:d} ".format(inter_sn, sn_x0)
                mycursor.execute(query11)

            mydb.commit()

            return(result_query1_int)

        # mycursor.rowcount != 0: find the 1st row of this sn, and update sn from 1st to 10th row;
        else:
            print("This SN has been tested before!")
            # query12: re-write the sn to 10 * row
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="mac_status")
            mycursor = mydb.cursor()

            # get the 1st row # of this sn
            mycursor.execute(query0)
            result_query0_one = mycursor.fetchone()
            result_query0_int = result_query0_one[0]

            print(3, result_query0_one[0])
            print(4, result_query0_int)

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="mac_status")
            mycursor = mydb.cursor()

            for sn_x1 in range(result_query0_int, result_query0_int+10):
                query12 = " UPDATE mac_spinel SET sn = '{0:s}' WHERE id = {1:d} ".format(inter_sn, sn_x1)
                mycursor.execute(query12)

            mydb.commit()
            return(result_query0_int)
    except:
        print("operate mysql db error")
    finally:
        # mycursor.close()
        # mydb.close()
        print("Fetched the db row number and Get Mac address")


# search_free_mac 函数，计算在数据库mac_status里, mac_spinel的这个表里有多少剩余没有使用的MAC 地址。
#

def search_free_mac():
    # query0: search the scanned sn is existed in mac_spinel table or not
    # query01: search the free in the mac_spinel table or not
    internal_free = "free"
    query01 = "SELECT * FROM mac_spinel WHERE sn = '{0:s}'".format(internal_free)

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="mac_status")
        mycursor = mydb.cursor()


        # get all the rowcount of this sn
        mycursor.execute(query01)
        result_query0_all = mycursor.fetchall()
        available_mac = mycursor.rowcount
        print(available_mac)
        return available_mac

    except:
        print("operate mysql db error")
    finally:
        # mycursor.close()
        # mydb.close()
        print("Fetched the db row number and Get Mac address")