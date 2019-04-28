'''
已知12306中站名使用字母表示的，显示时再转换成具体的中文
在https://kyfw.12306.cn/otn/resources/js/framework/进行查询时，可以看到js加载过程，发现有一个带有station_name字样的js
打开后发现就是我们要的字母和中文站名的对应表
https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9099
'''

import requests, re, json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9099'
r = requests.get(url=url, headers=headers)

data = re.findall(r'([\u2E80-\u9FFF]{2,3})\|([A-Z]+)', r.text) #匹配中文和对应字符

station_code = dict(data) #站名为key
station_name = dict(zip(station_code.values(), station_code.keys()))#字母为key

with open('station_code.json', 'w') as f:
    json.dump(station_code, f)
with open('station_name.json', 'w') as f:
    json.dump(station_name, f)
