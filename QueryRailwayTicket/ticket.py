import requests, json
import prettytable as pt

#通过url返回查询结果
def get_info(url):
    try:
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        r = requests.get(url=url, headers=headers)
        return(r.text)
    except Exception as e:
        print("获取网页信息失败:", e)

#解析返回的html
def showTicket(html):
    data = json.loads(html)
    table = pt.PrettyTable()
    table.field_names = [" 车次 ","出发站台","到达站台","出发时间","到达时间"," 历时 "," 商务座","一等座","二等座",
                         "高级软卧","软卧","硬卧","软座","硬座","无座"]
    for i in data["data"]["result"]:
        name = [
            "train_number",
            "start_station",
            "end_station",
            "start_time",
            "end_time",
            "duration",
            "swz",
            "ydz",
            'edz',
            "gjrw",
            'rw',
            'yw',
            'rz',
            'yz',
            'wz'
        ]

        data = {
            "train_number": '',
            "start_station": '',
            "end_station": '',
            "start_time": '',
            "end_time": '',
            "duration": '',
            "swz": '',
            "ydz": '',
            'edz': '',
            "gjrw": '',
            'rw': '',
            'yw': '',
            'rz': '',
            'yz': '',
            'wz': ''
        }
        item = i.split('|')

        data["train_number"]  = item[3] #车次
        data["start_station"] = item[4]
        data["end_station"]   = item[5]
        data["start_time"]    = item[8]
        data["end_time"]      = item[9]
        data["duration"]      = item[10]
        data["swz"]           = item[32] or item[25] #商务座
        data["ydz"]           = item[30]#一等座
        data["edz"]           = item[31]#二等座
        data["gjrw"]          = item[21]#高级软卧
        data["rw"]            = item[23]
        data["yw"]            = item[27]
        data["rz"]            = item[24]
        data["yz"]            = item[29]
        data["wz"]            = item[26]
        #没有信息的用'-'替代
        for i in name:
            if data[i]=='':
                data[i]='-'
        tickets = []
        for i in name:
            tickets.append(data[i])
        table.add_row(tickets)
    print(table)


if __name__=="__main__":
    train_date = "2019-05-01"
    url = f"https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT"
    html = get_info(url)
    showTicket(html)

