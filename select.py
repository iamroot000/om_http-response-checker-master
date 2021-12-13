import sys
import time
import datetime
import requests
from delete import _delete
import mysql.connector
from mysql.connector import Error
from check_send import _checker
from smtp_send import sendMail
import subprocess, os
import ipaddress


def _resolveip(mydomain):
    out_list = []
    _domain = mydomain.replace('https://', '').replace('http://', '').strip()
    _dns = "8.8.8.8"
    _out = os.popen("nslookup {} {}".format(_domain, _dns))
    for i in _out.read().split('\n'):
        if len(i) != 0:
            out_list.append(i)

    try:
        nsnum = -1
        myip = ipaddress.ip_address(unicode(out_list[nsnum].split('Address:')[-1].strip()))
        while True:
            if len(str(myip).split(':')) > 1:
                nsnum = nsnum - 2
                myip = ipaddress.ip_address(unicode(out_list[nsnum].split('Address:')[-1].strip()))
                # print(nsnum)
            else:
                return myip
    except Exception as e:
        return None



def _resolveip2(mydomain):
    _domain = mydomain.replace('https://', '').replace('http://', '').strip()
    _split = "PING".format(_domain)
    _split2 = "bytes of data"
    try:
        args = "ping -c1 -W1 {}".format(_domain)
        child = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
        out, err = child.communicate()
        # print("this is the output of command {}".format(out.split(_split)[-1].split()[1].strip().replace('(', '').replace(')', '')))
        # out_list = out.split(_split)[-1].split(_split2)[0].strip().split()[0].replace('(', '').replace(')', '')
        out_list = out.split(_split)[-1].split()[1].strip().replace('(', '').replace(')', '')
        print("resolve result is {}".format(out_list))
        return out_list
    except Exception as e:
        print("PING IP ERROR {}".format(str(e)))
        return None



def _curlping(url):
    _nsresult = _resolveip2(url)
    _status_code = ['200', '403', '301', '404']
    if _nsresult == None or _nsresult == "None":
        print("ERROR not RESOLVE")
        return 0
    else:
        # print("CURL resolve {}".format(_nsresult))
        args = "curl --write-out '{}' --resolve {}:443:{} -s {} --max-time 15 --silent --output /dev/null".format("%{http_code}",
            url.replace('https://', '').replace('http://', '').strip(), _nsresult, url)
        print("CURL PING COMMAND: {}".format(args))
        child = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
        out, err = child.communicate()
        if str(out) not in _status_code:
            return 0
        else:
            return 1





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
        zdb.close()
        zm_cursor.close()
    except Error as e:
        print("Error reading data from MySQL table", e)
#    finally:
#        if (zdb.is_connected()):
#            zdb.close()
#            zm_cursor.close()


def _select():
    try:
        adb = mysql.connector.connect(
            host="10.165.22.205",
            user="argususer2",
            passwd="c3phcl13nt",
            database="argus_v2"
        )

        argus_cursor = adb.cursor()

        argus_cursor.execute(
			"SELECT domain from SSLDOMAINS_ssldomain2 where domain not in ( 'v2r-sz1.qlinlin.top', 'alusa.zhubb.top' ,'font30.hahaszj.top' ,'v2r-sz2.qlinlin.top', '51m.fun', 'fpms_sslserver_key.neweb.me', 'fpms_sslserver.neweb.me', 'elog.yunduan123.cn', 'euftp.497g.com', 'www.paysage.site' ) and skip='no'")

        res = argus_cursor.fetchall()
        # res = ["cstest.payhome.site", "devoffice99.fpms8.me", "office-test.fpms8.me", "agent-test.payhome.site", "www99.payhome.site", "omtools.me", "papi-pccw2.fpms8.me"]
        print("Total number of Domain is: ", argus_cursor.rowcount)
        for r in res:

            url = "https://%s" % (r)
            try:
                rr = requests.get(url, timeout=15)
                # print("{} - {}".format(str(r), rr))
                if int(rr.status_code) == 502:
                    print("{} try ========= {} - {}".format("1st",str(r), rr.status_code))
                    _insert(url, status="1")
                    for i in range(0, 3):
                        time.sleep(10)
                        try:
                            rr = requests.get(url, timeout=15)
                            # print("{} - {}".format(str(r), rr))
                            if int(rr.status_code) == 502:
                                print("{} try ========= {} - {}".format(i, str(r), rr.status_code))
                                _insert(url, status="1", insertme=False)
                            else:
                                _insert(url, status="0", insertme=False)
                                break
                        except Exception as e:
                            _nsresult = _resolveip(url)
                            if _nsresult == None or _nsresult == "None":
                                print("{} try ========= {}".format(i, str(e)))
                                _insert(url, status="1", insertme=False)
                            else:
                                args = ["curl", "--resolve",
                                        "{}:443:{}".format(url.replace('https://', '').replace('http://', '').strip(),
                                                           _nsresult), "-I", url, "--max-time", "15"]
                                child = subprocess.Popen(args, stdout=subprocess.PIPE)
                                streamdata = child.communicate()[0]
                                rc = child.returncode
                                if int(rc) != 0:
                                    print("{} try ========= {}".format(i, str(e)))
                                    print(args)
                                    curlval = _curlping(url)
                                    print("CURLVAL: {}".format(curlval))
                                    if curlval == 1:
                                        _insert(url, status="0", insertme=False)
                                        break
                                    else:
                                        _insert(url, status="1", insertme=False)
                                else:
                                    # print("{} try ========= {}".format(i, str("{} - exit code {}".format(url, rc))))
                                    _insert(url, status="0", insertme=False)
                                    break
                else:
                    _insert(url, status="0")
            # except requests.ConnectionError, e:
            #     # Error / Failed
            #
            #     print(e)
            #     _insert(url, status="1")
            # except requests.exceptions.TooManyRedirects, e:
            #     print(e)
            #     _insert(url, status="1")
            except Exception as e:
                _insert(url, status="1")
                for i in range(0,3):
                    time.sleep(10)
                    try:
                        rr = requests.get(url, timeout=15)
                        # print("{} - {}".format(str(r), rr))
                        if int(rr.status_code) == 502:
                            print("{} try ========= {} - {}".format(i,str(r), rr.status_code))
                            _insert(url, status="1", insertme=False)
                        else:
                            _insert(url, status="0", insertme=False)
                            break
                    except Exception as e:
                        _nsresult = _resolveip(url)
                        if _nsresult == None or _nsresult == "None":
                            print("{} try ========= {}".format(i, str(e)))
                            _insert(url, status="1", insertme=False)
                        else:
                            args = ["curl", "--resolve",
                                    "{}:443:{}".format(url.replace('https://', '').replace('http://', '').strip(),
                                                       _nsresult), "-I", url, "--max-time", "15"]
                            child = subprocess.Popen(args, stdout=subprocess.PIPE)
                            streamdata = child.communicate()[0]
                            rc = child.returncode
                            if int(rc) != 0:
                                print("{} try ========= {}".format(i, str(e)))
                                print(args)
                                curlval = _curlping(url)
                                print("CURLVAL: {}".format(curlval))
                                if curlval == 1:
                                    _insert(url, status="0", insertme=False)
                                    break
                                else:
                                    _insert(url, status="1", insertme=False)
                            else:
                                # print("{} try ========= {}".format(i, str("{} - exit code {}".format(url, rc))))
                                _insert(url, status="0", insertme=False)
                                break

            # else:
            #     # Success





    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (adb.is_connected()):
            adb.close()
            argus_cursor.close()


if __name__ == '__main__':
    _delete()
    _select()

    email_subject = "HTTP Response Checker {}".format(datetime.datetime.now().strftime("%Y-%m-%d"))
    if len(_checker()) != 0:
        email_content = '''Hi All,

Please check these domains are inaccessible.

{}'''.format('\n'.join(_checker()))
    else:
        email_content = '''Hi All,

All Domains are Normal and Accessible.

{}'''.format('\n'.join(_checker()))

    #        email_content = '''Testing

    # {}'''.format('\n'.join(_checker()))

    print(sendMail(['omgroup@m1om.me'], email_subject, email_content))
    # print(sendMail(['yroll.macalino@m1om.me'], email_subject, email_content))



