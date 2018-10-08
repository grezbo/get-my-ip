#!/usr/bin/python3

import sqlite3
from urllib import request
from email.header import Header
from email.mime.text import MIMEText
import smtplib
import os
import time

DB_FILE = 'ip.db'


# icanhazip.com
def get_ip_from_icanhazip():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }
    url = 'http://icanhazip.com'
    req = request.Request(url, headers=header)
    resp = request.urlopen(req)
    ip = resp.read().decode('utf-8')

    return ip.strip()


def send_mail(content):
    from_addr = os.environ['EMAIL_ADDR']
    password = os.environ['EMAIL_PASSWD']
    to_addr = os.environ['TO_EMAIL_ADDR']
    smtp_server = os.environ['SMTP_SERVER']


    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = Header('ip地址变化', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def add_ip(ip_address):
    conn = sqlite3.connect(DB_FILE)
    conn.execute('create table if not exists wan_ip(id INTEGER PRIMARY KEY AUTOINCREMENT, create_time TEXT,ip TEXT)')
    conn.execute("insert into wan_ip (create_time, ip) values (datetime('now'), '" + ip_address + "')")
    conn.commit()
    conn.close()


def create_table():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('create table if not exists wan_ip(id INTEGER PRIMARY KEY AUTOINCREMENT, create_time TEXT,ip TEXT)')
    conn.close()


def get_last_ip():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('create table if not exists wan_ip(id INTEGER PRIMARY KEY AUTOINCREMENT, create_time TEXT,ip TEXT)')
    cursor = conn.execute('select t.ip from wan_ip t order by t.id desc limit 1')
    ip = ''
    for line in cursor:
        ip = line[0]
    conn.close()
    return ip


if __name__ == '__main__':
    interval = int(os.environ['INTERVAL'])
    # interval = 1
    while True:
        try:
            ip = get_ip_from_icanhazip()
            last_ip = get_last_ip()
            if ip == last_ip:
                pass
            else:
                add_ip(ip)
                send_mail(ip)
        except BaseException:
            pass
        time.sleep(interval)
