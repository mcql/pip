import requests
from bs4 import BeautifulSoup
import json
import time
import pymysql
import re


# 获取分类歌曲
def musiclist(url, typename, typepic, typeid):
    headers = {
        'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
        'Host':
            "music.163.com"
    }
    # 数据库连接
    db = pymysql.Connect(
        host='localhost',
        port=3307,
        user='root',
        passwd='123123',
        db='python_test',
        charset='utf8')
    cursor = db.cursor()
    # 发送请求
    response = requests.get(
        url,
        headers=headers,
        timeout=10,
        proxies={"http": "60.184.2.228" + ":" + "53128"})
    res = BeautifulSoup(response.text, 'html.parser')
    content = res.find("textarea", attrs={"id": "song-list-pre-data"}).text
    musicLists = json.loads(content)
    musicontent = []
    for musicList in musicLists:
        try:
            timeStamp = musicList.get("publishTime") / 1000
            timeArray = time.localtime(timeStamp)
            publishTime = time.strftime("%Y-%m-%d", timeArray)  # 发行时间
        except Exception:
            publishTime = ''

        commentsid = musicList.get("commentThreadId")  # 评论路径id
        id = musicList.get("id")  # 歌曲id
        musicname = musicList.get("name")  # 歌曲名称
        musicnamereg = re.sub(r'\"', '', musicname)
        musicauthor = musicList.get("artists")[0].get("name")  # 演唱者
        musicpic = musicList.get("album").get("picUrl")  # 歌曲封面
        realURL = r'http://music.163.com/song/media/outer/url?id=' + str(id)
        musicontent.append({
            "publishTime": publishTime,
            "commentsid": commentsid,
            "id": id,
            "musicname": musicnamereg,
            "musicauthor": musicauthor,
            "musicpic": musicpic,
            "realURL": realURL,
            "typename": typename,
            "typepic": typepic
        })
        # 插入数据库
        sql = 'INSERT INTO music VALUES(' + str(
            id
        ) + ',\"' + musicnamereg + '\","' + publishTime + '","' + commentsid + '","' + musicauthor + '","' + musicpic + '","' + realURL + '","' + typename + '","' + typepic + '","' + typeid + '")'
        # print(sql)
        cursor.execute(sql)
        db.commit()

    db.close()
    return musicontent


# 获取分类信息
def musictype(url):
    headers = {
        'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
        'Host':
            "music.163.com"
    }
    # 发送请求
    response = requests.get(
        url,
        headers=headers,
        timeout=10,
        proxies={"http": "60.184.2.228" + ":" + "53128"})
    db = pymysql.Connect(
        host='localhost',
        port=3307,
        user='root',
        passwd='123123',
        db='python_test',
        charset='utf8')
    cursor = db.cursor()
    res = BeautifulSoup(response.text, 'html.parser')
    rescontents = res.find_all("div", attrs={"class": "left"})
    typemusics = []
    for rescontent in rescontents:
        try:
            typeid = rescontent.parent.parent.get("data-res-id")
            typeurl = rescontent.find("a").get("href")
            typename = rescontent.find("img").get("alt")
            typepicsmall = rescontent.find("img").get("src")
            typepic = re.sub(r'40', '150', typepicsmall)
            if (typeid != None):
                typemusics.append({
                    "typeid": typeid,
                    "typeurl": typeurl,
                    "typename": typename,
                    "typepic": typepic
                })
        except Exception as e:
            print(e)

        if (typeid != None):
            sql = 'INSERT INTO musictype VALUES("' + str(
                typeid
            ) + '","' + typeurl + '","' + typename + '","' + typepic + '")'
            print(sql)
            cursor.execute(sql)
            db.commit()

    db.close()
    return typemusics


if __name__ == '__main__':
    typeurl = 'https://music.163.com/discover/toplist'
    for musicall in musictype(typeurl):
        url = 'https://music.163.com' + musicall.get("typeurl")  # 获取分类url
        typename = musicall.get("typename")  # 获取分类名称
        typepic = musicall.get("typepic")
        typeid = musicall.get("typeid")
        musiclist(url, typename, typepic, typeid)
        # 写入json文件
        with open("./music.json", "a", encoding='utf-8') as f:
            json.dump(
                musiclist(url, typename, typepic, typeid),
                f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True)
