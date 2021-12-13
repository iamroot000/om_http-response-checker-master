import sys
import datetime
import requests
from delete import _delete
import mysql.connector
from mysql.connector import Error



def _select():
	try:
		adb = mysql.connector.connect(
		                host="10.165.22.205",
                                user="argususer2",
                                passwd="c3phcl13nt",
                                database="argus_v2"
                                )

                argus_cursor = adb.cursor()

                #argus_cursor.execute("SELECT domain from SSLDOMAINS_ssldomain2 where domain not in ( 'v2r-sz1.qlinlin.top', 'alusa.zhubb.top' ,'font30.hahaszj.top' ,'v2r-sz2.qlinlin.top' )")
                argus_cursor.execute("SELECT domain from SSLDOMAINS_ssldomain2")


                res = argus_cursor.fetchall()
                print("Total number of rows in Laptop is: ", argus_cursor.rowcount)
        except Error as e:
                 print("Error reading data from MySQL table", e)
        finally:
                if ( adb.is_connected()):
                        adb.close()
                        argus_cursor.close()




def _insert():
        try:
                zdb = mysql.connector.connect(
                                host="10.165.22.205",
                                user="argususer2",
                                passwd="c3phcl13nt",
                                database="zmonitor"
                                )
                zm_cursor = zdb.cursor()
                #sql = "SELECT domain from SSLDOMAINS_ssldomain2 where domain not in ( 'v2r-sz1.qlinlin.top', 'alusa.zhubb.top' ,'font30.hahaszj.top' ,'v2r-sz2.qlinlin.top' )"
		#sql = "SELECT domain from curlresult where domain not in ( 'https://v2r-sz1.qlinlin.top', 'https://alusa.zhubb.top' ,'https://font30.hahaszj.top' ,'https://v2r-sz2.qlinlin.top' )"
		sql = "SELECT domain from curlresult"
	
                zm_cursor.execute(sql)
                res = zm_cursor.fetchall()
                print("Total number of rows in Laptop is: ", zm_cursor.rowcount)
        except Error as e:
                 print("Error reading data from MySQL table", e)
        finally:
                if ( zdb.is_connected()):
                        zdb.close()
                        zm_cursor.close()




def _delete():
        try:
                zdb = mysql.connector.connect(
                                host="10.165.22.205",
                                user="argususer2",
                                passwd="c3phcl13nt",
                                database="zmonitor"
                                )
                zm_cursor = zdb.cursor()
		sql = "DELETE FROM curlresult WHERE domain IN ( 'https://v2r-sz1.qlinlin.top', 'https://alusa.zhubb.top' ,'https://font30.hahaszj.top' ,'https://v2r-sz2.qlinlin.top' )"
                zm_cursor.execute(sql)
                zdb.commit()
        except Error as e:
                 print("Error reading data from MySQL table", e)
        finally:
                if ( zdb.is_connected()):
                        zdb.close()
                        zm_cursor.close()


if __name__=='__main__':
	_select()
	_insert()
        _delete()




