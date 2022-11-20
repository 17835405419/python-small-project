"""
作者：zwq
日期:2022年03月06日
"""
import requests
import json
import os



headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'csrf': 'HH88ZEOF6WT',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Referer': 'http://www.kuwo.cn/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

cookies = {
    '_ga': 'GA1.2.1085958577.1646568038',
    '_gid': 'GA1.2.1276314754.1646568038',
    'Hm_lvt_cdb524f42f0ce19b169a8071123a4797': '1646568038,1646568060',
    'Hm_lpvt_cdb524f42f0ce19b169a8071123a4797': '1646568060',
    '_gat': '1',
    'kw_token': 'HH88ZEOF6WT',
}

# 代理
# proxies = {
#     "http": "http://211.65.197.93:80"
# }





def jsonparser(text):
    js = dict(json.loads(text))
    return js


# 下载文件
def write_file(song_name, song_title, author, content):
        with open(f"下载酷我音乐/{song_name}/{song_title}---{author}.mp3",mode='wb') as f:
            f.write(content)





def main(song_name,song_num):
    song_name = song_name
    song_num = song_num
    if not os.path.exists(f"下载酷我音乐/{song_name}"):
        os.mkdir(f"下载酷我音乐/{song_name}")
    else:
        err = '该文件夹已存在'
        return err

    url = f'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={song_name}&pn=1&rn={song_num}&httpsStatus=1&reqId=7328a2f1-9d45-11ec-b584-efbc7543ad33'

    res = requests.get(url, headers=headers,cookies=cookies)
    songList_js = jsonparser(res.text)

    change_name = []
    for song in songList_js["data"]["list"]:
        song_title = song['name']
        author = song['artist']
        song_id = song['rid']
        change_name.append(song_title +"       "+ author)
        # 获取歌曲的播放链接
        song_url = f"http://www.kuwo.cn/api/v1/www/music/playUrl?mid={song_id}&type=music&httpsStatus=1&reqId=64b316e1-9d47-11ec-8150-7177269a35ab"
        song_resp = requests.get(song_url,headers=headers,cookies=cookies)
        # 处理json数据
        song_js = jsonparser(song_resp.text)
        if song_js["code"] == -1:
            print(song_js["msg"])
        else:
            song_player_url = song_js["data"]["url"]
            # 请求该歌曲 获取二进制数据
            song_content = requests.get(song_player_url, cookies=cookies, headers=headers)
            # 写入操作
            write_file(song_name, song_title, author, song_content.content)
    return change_name



