import sys
import datetime
import requests
import mysql.connector
from mysql.connector import Error



def _checker():
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
			print r

        except Error as e:
                 print("Error reading data from MySQL table", e)
        finally:
                if ( zdb.is_connected()):
                        zdb.close()
                        zm_cursor.close()
                        print ("MySQL connection is closed")


if __name__=='__main__':
	_checker()

