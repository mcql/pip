import requests
import json
import time
import pymysql

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36"
}

db = pymysql.Connect(
    host='localhost',
    port=3307,
    user='root',
    passwd='123123',
    db='wy_music',
    charset='utf8')
cursor = db.cursor()


# 获取分页数量
def countpage(id):
    response = requests.get(
        'https://music.163.com/api/v1/resource/comments/R_SO_4_' + id +
        '?limit=100&offset=0',
        headers=headers)
    res = json.loads(response.text)
    page = int(res['total'] / 100)
    return page


def mysql(data):
    # sql拼接
    sql = 'INSERT INTO comments VALUES(null , ' + str(
        data['userId']) + ',\"' + str(data['nickname']) + '\",\"' + str(
            data['avatarUrl']) + '\",' + str(data['likedCount']) + ',' + str(
                data['commentId']) + ',\"' + str(data['time']) + '\",\"' + str(
                    data['content']) + '\",' + str(
                        data['userType']) + ',' + str(data['vipType']) + ')'
    return sql


# 获取所有评论
def comments(page, id):
    # 循环遍历每页评论
    for i in range(0, page + 1):
        url = 'https://music.163.com/api/v1/resource/comments/R_SO_4_' + id + '?limit=100&offset=' + str(
            i * 100)
        response1 = requests.get(url, headers=headers)
        res1 = json.loads(response1.text)
        contents = res1['comments']
        for content in contents:
            # 写入文件
            filename = 'testpl.txt'
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(content['user']['nickname'] + ':' + content['content'] +
                        '\n' + ' ' + url)
            # 写入数据库
            data = {
                "userId": content['user']['userId'],
                "nickname": content['user']['nickname'],
                "avatarUrl": content['user']['avatarUrl'],
                "likedCount": content['likedCount'],
                "commentId": content['commentId'],
                "time": content['time'],
                "content": content['content'],
                "userType": content['user']['userType'],
                "vipType": content['user']['vipType']
            }
            try:
                cursor.execute(mysql(data))
                db.commit()
            except Exception as e:
                print(e)
        print(i)


# 执行
if __name__ == '__main__':
    id = '1318234987'  # 歌名对应的id
    comments(countpage(id), id)
    db.close()
    print("爬取完成")
