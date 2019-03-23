'''
最近在看一部连载中的小说，每天查更新太累了，
决定写个自查脚本，推送更新到邮箱
'''

from pyquery import PyQuery as pq
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import requests, time, smtplib

'''
获取小说的章节目录
发起请求最好都加上一个异常捕获
'''
def get_catalog(url):
    try:
        r = requests.get(url)
        r.encoding = "gbk"
        return r.text
    except ConnectionError as e:
        print(e, "获取章节目录失败")


'''
检查是否有更新
为了避免作者一次更新两章
我的解决办法是每次获取最新的十章来进行比较
返回带有未读章节的url
'''
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

'''
解析最新的章节页
只留下文章标题和具体内容
剩下花里胡哨的就不要了
'''
def parse_chapter(url):
    try:
        r = requests.get(url)
        r.encoding = "gbk"
        doc = pq(r.text)
        title = doc('h1')
        content = doc('.contentbox.clear')
        return str(title)+str(content)
    except ConnectionError as e:
        print(e, "解析文章内容失败")
'''
发送邮件
qq邮箱的密码就是授权码
涉及隐私我的就匿了
邮件部分参考了廖雪峰老师的教程
'''
def send_email(urls):
    from_addr = "from@qq.com"
    password = "在自己的邮箱获取"
    to_addr = "接收邮箱"
    smtp_server = "smtp.qq.com"
    for url in urls:
        temp = url
        html = parse_chapter(url)
        # msg接受的是str类型
        msg = MIMEText(html, 'html', 'utf-8')

        msg['From'] = formataddr(("幻月书院", from_addr)) #发件人
        msg['To'] = formataddr(("mumu157", to_addr))   #收件人
        msg['Subject'] = "小说更新啦"   #主题

        try:
            server = smtplib.SMTP_SSL(smtp_server, 465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
            print("成了")
        except smtplib.SMTPException as e:
            print('发送失败', e)

    with open('temp.txt', 'w', encoding='gbk') as f:
        f.write(temp)#把最新章节存入缓存文件当中

'''
接下来就是主函数了
url是小数的章节目录
然后将当前已读章节的url存入本地缓存
如果检测到有更新的小说
程序会休息8小时再工作，否则每小时检查一次
'''
if __name__=="__main__":
    url = "http://www.huanyue123.com/book/37/37849/"
    with open('temp.txt', 'w', encoding="gbk") as f:
        temp = f.write("http://www.huanyue123.com/book/37/37849/28582591.html")
    while True:
        r = get_catalog(url)
        urls = check_chapter(r)
        if len(urls)!=0:
            send_email(urls)
            time.sleep(28800)
        else:
            print("没有更新的小说哦")
            time.sleep(3600)