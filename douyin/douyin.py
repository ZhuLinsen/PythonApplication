import os, json, requests
import time

headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

def download():
    json_list = os.listdir('.\\url_list')
    if len(json_list)>0:
        for j in json_list:
            with open(f'.\\url_list\\{j}', 'r', encoding='utf-8') as f:
                try:
                    content = json.load(f)['aweme_list']
                except:
                    pass

            for i in content:
                try:
                    title = i['desc'][:10] #文件名
                    url = i['video']['play_addr']['url_list'][1]#获取视频链接
                    name = f'.\\video\\{title}.mp4'
                    if not os.path.exists(path=name):
                        try:
                            r = requests.get(url, headers=headers)
                            with open(name, 'wb') as f:
                                f.write(r.content)
                            print(title + ' 下载完成')
                        except Exception as e:
                            print(e, f"{title} 视频获取失败啦")
                    continue
                except:
                    pass
            if os.path.exists(f'.\\url_list\\{j}'):
                os.remove(f'.\\url_list\\{j}')
    else:
        print("快刷，没有更多视频了")
        time.sleep(15)

if __name__=="__main__":
    while True:
        download()
        time.sleep(25)