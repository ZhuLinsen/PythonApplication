'''
最近在看一部连载中的小说，每天查更新太累了，
决定写个自查脚本，推送更新到邮箱
'''

from pyquery import PyQuery as pq
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from threading import Thread, Lock
import requests, time
import logging

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

logging.basicConfig(level=logging.INFO, filename='Fiction_log.txt', filemode='a', format='%(asctime)s - %(message)s')

name = {"zhuixu": "赘婿",
        "mushenji": "牧神记"}

lock = Lock()

#获取章节目录
def get_catalog(url):
    try:
        r = requests.get(url, headers=headers)
        r.encoding = "gbk"
        return r.text
    except ConnectionError as e:
        print(e, "获取章节目录失败")

#检查是否有新章节
def check_chapter(html, fiction_name):
    doc = pq(html)
    lis = doc(".book_list ul li a")
    li = []
    for item in lis.items():
        li.append(item.attr.href)
    with open(f'{fiction_name}.txt', 'r', encoding="gbk") as f:
        temp = f.read()
    latest = li[-10:] #最新的十个章节
    print(latest)
    index = latest.index(temp)
    return latest[index+1:]

#获取章节的内容
def parse_chapter(url):
    try:
        r = requests.get(url, headers=headers)
        r.encoding = "gbk"
        doc = pq(r.text)
        title = doc('h1')
        content = doc('.contentbox.clear')
        logging.info(f'章节 {title} 解析成功，url为 {url}')
        return str(title)+str(content)
    except ConnectionError as e:
        print(e, "解析文章内容失败")
#发送邮件
def send_email(urls, fiction_name):
    from_addr = "*****@qq.com"
    password = "*****"
    to_addr = "*****@qq.com"
    smtp_server = "smtp.qq.com"
    for url in urls:
        temp = url
        html = parse_chapter(url)
        msg = MIMEText(html, 'html', 'utf-8') #msg接受的是str类型

        #msg['From'] = formataddr((Header("我是发件者", "utf-8").encode(), from_addr))
        msg['From'] = formataddr(("幻月书院", from_addr))
        msg['To'] = formataddr(("mumu157", to_addr))
        msg['Subject'] = f" {name[fiction_name]} 更新啦"

        try:
            lock.acquire()
            server = smtplib.SMTP_SSL(smtp_server, 465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
            logging.info(f'章节 {url} 发送成功\n')
            print("发送成功")
        except smtplib.SMTPException as e:
            print('发送失败', e)
        finally:
            lock.release()

    with open(f'{fiction_name}.txt', 'w', encoding='gbk') as f:
        f.write(temp)#把最新章节存入缓存文件当中
        logging.info(f'正在将最新章节 {temp} 写入本地缓存\n')

def main(url, fiction_name):
    while True:
        print(f"正在检测{name[fiction_name]}")
        r = get_catalog(url)
        print(r[:100])
        url_ch = check_chapter(r, fiction_name)
        if len(url_ch)!=0:
            send_email(url_ch, fiction_name)
            time.sleep(28800)
        else:
            print("没有更新的小说哦")
            time.sleep(1800)

if __name__=="__main__":
    url_mushenji = "http://www.huanyue123.com/book/37/37849/"#牧神记章节目录列表
    url_zhuixu = "http://www.huanyue123.com/book/1/1822/"  # 赘婿章节目录列表
    with open('mushenji.txt', 'w', encoding="gbk") as f:
        temp = f.write("http://www.huanyue123.com/book/37/37849/29466353.html")
    with open('zhuixu.txt', 'w', encoding="gbk") as f:
        temp = f.write("http://www.huanyue123.com/book/1/1822/29411339.html")
    t1 = Thread(target=main, args=(url_mushenji, 'mushenji'))
    t2 = Thread(target=main, args=(url_zhuixu, 'zhuixu'))
    t1.start()
    t2.start()
    t1.join()
    t2.join()