'''
检测微信好友是否单项删除了你
测试需谨慎，结果很扎心
'''

import itchat, time

print("测试需谨慎 结果很扎心")

input("输入任意键继续...")

itchat.auto_login(hotReload=True)
#itchat.auto_login(enableCmdQR=2)


friends = itchat.get_friends(update=True)

length = len(friends)

for i in range(1, length):

    itchat.send("జ్ఞా", toUserName=friends[i]['UserName'])
    print(f'检测到第{i}位好友: {str(friends[i]["NickName"]).center(20, " ")}')
    #print(friends[i]['UserName'])
    time.sleep(2.5)

print("测试已完成")

itchat.run()
