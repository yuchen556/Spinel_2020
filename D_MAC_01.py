import mysql.connector
# 将所有行都变为free 关键字

def update_sn():
    # prepare query and data

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="mac_status")

    mycursor = mydb.cursor()
    for xxx in range(1, 101):
        query = "UPDATE mac_spinel SET sn = '{0:s}' WHERE id = {1:d}".format("free", xxx)
        mycursor.execute(query)

    mydb.commit()


update_sn()