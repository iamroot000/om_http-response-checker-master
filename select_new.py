import sys
import time
import datetime
import requests
from delete import _delete
import mysql.connector
from mysql.connector import Error
from check_send import _checker
from smtp_send import sendMail
from nslookup import Nslookup
import subprocess



def _resolveip(mydomain):
    _dns = ["8.8.8.8"]
    _domain = mydomain.replace('https://', '').replace('http://', '').strip()
    dns_query = Nslookup(dns_servers=_dns)
    ips_record = dns_query.dns_lookup(_domain)
    ip = ips_record.answer

    if len(ip) == 0:
        for i in range(0,3):
            time.sleep(10)
            ips_record = dns_query.dns_lookup(_domain)
            ip = ips_record.answer
            if len(ip) != 0:
                out_ip = ip[-1]
                # print("try {} -----> {} = {}".format(i,_domain, out_ip))
                return out_ip
            else:
                out_ip = None
                # print("ERROR try {} -----> {} = {}".format(i, _domain, out_ip))
    else:
        out_ip = ip[-1]
        # print("{} = {}".format(_domain, out_ip))
        return out_ip




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
            "SELECT domain from SSLDOMAINS_ssldomain2 where domain not in ( 'v2r-sz1.qlinlin.top', 'alusa.zhubb.top' ,'font30.hahaszj.top' ,'v2r-sz2.qlinlin.top', '51m.fun', 'fpms_sslserver_key.neweb.me', 'fpms_sslserver.neweb.me' )")

        # res = argus_cursor.fetchall()
        res = ["www.kinsdsdsgbally.com", "12858888.com", "12898888.com", "www.deli13145.com"]
        print("Total number of rows in Laptop is: ", argus_cursor.rowcount)
        for r in res:

            url = "https://%s" % (r)
            try:
                rr = requests.get(url, timeout=10)
                # print("{} - {}".format(str(r), rr))
                if int(rr.status_code) == 502:
                    print("{} try ========= {} - {}".format("1st",str(r), rr.status_code))
                    _insert(url, status="1")
                    for i in range(0, 3):
                        time.sleep(10)
                        try:
                            rr = requests.get(url, timeout=10)
                            # print("{} - {}".format(str(r), rr))
                            if int(rr.status_code) == 502:
                                print("{} try ========= {} - {}".format(i, str(r), rr.status_code))
                                _insert(url, status="1", insertme=False)
                            else:
                                _insert(url, status="0", insertme=False)
                                break
                        except Exception as e:
                            _nsresult = _resolveip(url)
                            if _nsresult == None:
                                print("{} try ========= {}".format(i, str(e)))
                                _insert(url, status="1", insertme=False)
                            else:
                                args = ["curl", "--resolve",
                                        "{}:443:{}".format(url.replace('https://', '').replace('http://', '').strip(),
                                                           _nsresult), "-I", url]
                                child = subprocess.Popen(args, stdout=subprocess.PIPE)
                                streamdata = child.communicate()[0]
                                rc = child.returncode
                                if int(rc) != 0:
                                    print("{} try ========= {}".format(i, str(e)))
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
                        rr = requests.get(url, timeout=10)
                        # print("{} - {}".format(str(r), rr))
                        if int(rr.status_code) == 502:
                            print("{} try ========= {} - {}".format(i,str(r), rr.status_code))
                            _insert(url, status="1", insertme=False)
                        else:
                            _insert(url, status="0", insertme=False)
                            break
                    except Exception as e:
                        _nsresult = _resolveip(url)
                        if _nsresult == None:
                            print("{} try ========= {}".format(i, str(e)))
                            _insert(url, status="1", insertme=False)
                        else:
                            args = ["curl", "--resolve",
                                    "{}:443:{}".format(url.replace('https://', '').replace('http://', '').strip(),
                                                       _nsresult), "-I", url]
                            child = subprocess.Popen(args, stdout=subprocess.PIPE)
                            streamdata = child.communicate()[0]
                            rc = child.returncode
                            if int(rc) != 0:
                                print("{} try ========= {}".format(i, str(e)))
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

    # print(sendMail(['omgroup@m1om.me'], email_subject, email_content))
    print(sendMail(['yroll.macalino@m1om.me'], email_subject, email_content))

