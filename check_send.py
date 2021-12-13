import sys

import datetime

import requests

import json

import mysql.connector

from mysql.connector import Error

import smtplib

from email.mime.application import MIMEApplication

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from email.utils import COMMASPACE, formatdate





def _checker():

    # rVal = {

    #     "data" : []

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

            #     "{#DOMAIN}" : str(r[-1]),

            #     "{#STATUS}": 1})

            data.append(r[-1])





    except Error as e:

             return "Error reading data from MySQL table".format(str(e))

    finally:

            if ( zdb.is_connected()):

                    zdb.close()

                    zm_cursor.close()

                    # print ("MySQL connection is closed")

                    # return "MySQL connection is closed"

    return data







#attachments = {"filename":"content"};

def sendMail(send_to, subject, text, files={},server="smtp.gmail.com",port=587):

    username = "noreply@m1om.me"

    password = "bananaballs123!"

    assert isinstance(send_to, list);

    msg = MIMEMultipart();

    msg['From'] = username;

    msg['To'] = COMMASPACE.join(send_to);

    msg['Date'] = formatdate(localtime=True);

    msg['Subject'] = subject;

    msg.attach(MIMEText(text));

    for i in files:

        part = MIMEApplication(

                files[i],

                Name=i

            );

        part['Content-Disposition'] = 'attachment; filename="%s"' % i;

        msg.attach(part);

    smtp = smtplib.SMTP();

    smtp.connect(server,port);

    smtp.starttls();

    smtp.login(username,password);

    smtp.sendmail(username,send_to,msg.as_string());

    smtp.close();

    return True;





def formatServiceInterruptionMSG(message):

    pass





if __name__=='__main__':

    email_subject = "Test Send"

    # email_content = '''Hi All,

    # Please check these domains are inaccessible.

    # {}'''.format(_checker())

    email_content = '''Testing

    {}'''.format('\n'.join(_checker()))

    print(sendMail(['yroll.macalino@m1om.me'], email_subject, email_content))

