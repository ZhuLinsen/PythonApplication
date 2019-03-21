'''
最近在看一部连载中的小说，每天查更新太累了，
决定写个自查脚本，推送更新到邮箱
'''

from pyquery import PyQuery as pq
import requests

#获取章节目录
def get_html(url):
    try:
        r = requests.get(url)
        r.encoding = "gbk"
        return r.text
    except ConnectionError as e:
        print(e, "获取章节目录失败")

#检查是否有更新
def check_chapter(html):
    doc = pq(html)
    lis = doc(".book_list ul li a")
    li = []
    for item in lis.items():
        li.append(item.attr.href)
    with open('temp.txt', 'r', encoding="gbk") as f:
        temp = f.read()
    latest = li[-10:]
    index = latest.index(temp)
    return latest[index+1:]

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(url):
    from_addr = "1225937029@qq.com"
    password = "jyixpmlpgjiegbcc"
    to_addr = "2920263131@qq.com"
    smtp_server = "smtp.qq.com"

    msg = MIMEText(url, 'plain', 'utf-8')
    msg['From'] = Header("小说更新啦<{}>".format(from_addr), "utf-8")
    msg['To'] = Header("花满楼<{}>".format(to_addr), "utf-8")
    msg['Subject'] = Header("小说更新咯", "utf-8")
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        print("成了")
    except smtplib.SMTPException as e:
        print('发送失败', e)


if __name__=="__main__":
    url = "http://www.huanyue123.com/book/37/37849/"
    r = get_html(url)
    urls = check_chapter(r)
    if len(urls)!=0:
        send_email(str(urls))