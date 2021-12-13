import sys
import datetime
import requests
import json
import mysql.connector
from mysql.connector import Error





def _checker():
    # rVal = {
    #
    #     "data": []
    #
    # }
    data = []

    try:
        zdb = mysql.connector.connect(
            host="10.165.22.205",
            user="argususer2",
            passwd="c3phcl13nt",
            database="zmonitor"
        )

        zm_cursor = zdb.cursor()
        sql = "select domain from curlresult where status='1'"
        zm_cursor.execute(sql)
        res = zm_cursor.fetchall()



        for r in res:
            # rVal["data"].append({
            #
            #     "{#DOMAIN}": str(r[-1]),
            #
            #     "{#STATUS}": 1})
            data.append(r[-1])


    except Error as e:
        return "Error reading data from MySQL table".format(str(e))



    finally:
        if (zdb.is_connected()):
            zdb.close()
            zm_cursor.close()
            # print ("MySQL connection is closed")
            # return "MySQL connection is closed"



    return data



def _zabbixData():
    rVal = {

        "data": []

    }

    try:
        zdb = mysql.connector.connect(
            host="10.165.22.205",
            user="argususer2",
            passwd="c3phcl13nt",
            database="zmonitor"
        )

        zm_cursor = zdb.cursor()
        sql = "select domain from curlresult where status='1'"
        zm_cursor.execute(sql)
        res = zm_cursor.fetchall()



        for r in res:
            rVal["data"].append({
                "{#DOMAIN}": str(r[-1]),
                "{#STATUS}": 1})



    except Error as e:
        return "Error reading data from MySQL table".format(str(e))
    
    return rVal

if __name__ == '__main__':
    # print('\n'.join(_checker()))
    print(json.dumps(_zabbixData(), indent=4))
