import mysql.connector

from mysql.connector import Error







def _insert(r, status, insertme=True):

    try:

        zdb = mysql.connector.connect(

            host="10.165.22.205",

            user="argususer2",

            passwd="c3phcl13nt",

            database="zmonitor"

        )

        zm_cursor = zdb.cursor()        

        if insertme:

            val = (r, status)

            sql = "insert into curlresult ( domain , status ) VALUES (%s, %s)"

        else:

            val = (status, r)

            sql = "update curlresult set status=%s where domain=%s"

        zm_cursor.execute(sql, val)

        zdb.commit()

    except Error as e:

        print("Error reading data from MySQL table", e)

    finally:

        if (zdb.is_connected()):

            zdb.close()

            zm_cursor.close()



if __name__ == '__main__':

    _insert("https://sslserver.fpms8.me", 3, insertme=False)
