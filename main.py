import requests, os, time, logging, re, random
from bs4 import BeautifulSoup


def login(host):
    url = host + "member.php"
    querystring = {"mod": "logging", "action": "login", "loginsubmit": "yes", "infloat": "yes", "lssubmit": "yes",
                   "inajax": "1"}
    payload = "fastloginfield=username&username=sky367&cookietime=2592000&password=ys3670825&quickforward=yes" \
              "&handlekey=ls "
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "aae6a852-9f6c-2c0f-25dd-ac7b2ea2f7d0"
    }
    session2 = requests.session()
    res = session2.request("POST", url, data=payload, headers=headers, params=querystring)
    return session2


# 列表页
def getList(host, url, session):
    res = session.get(host + url)
    soup = BeautifulSoup(res.text, 'html.parser')
    blocks = soup.find_all('a', class_='z')
    for b in blocks:
        url = host + b.attrs['href']
        getOne(host, url, session)
        # logging.info(url)


# 详情页
def getOne(host, url, session):
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    # 发表评论
    pushComment(url, session, soup)
    # 下载图片
    title = str.split(soup.title.text, " ")
    logging.info(title[0])
    folder = mkdirx(title[0])
    blocks = soup.find_all('img', file=re.compile('data/attachment/forum'))
    logging.info(len(blocks))
    for x in blocks:
        path = host + x.attrs['zoomfile']
        downloadPic(path, folder)
    logging.info('done')



def pushComment(url, session, soup):
    dicts = [
        "守望着天空，大海，和你的回忆。",
        "潮水中沉没着被遗忘的名字，它们溺死于自作多情的泡沫。",
        "在我手里，正义从不会迟到半秒。",
        "空洞和孤独，依靠温暖的灯光填补。",
        "有种愚弄自己的东西，叫忠诚。",
        "破碎的奇迹好过没有，苦恼的希望胜于迷茫。",
        "你整个人都是注水的。",
        "守护爱人的心，因恐惧失去而污秽。",
        "点亮的星，不会轻易熄灭。",
        "守望着天空、大海和你的回忆。",
        "完美，是最无情的禁锢。",
        "逆流而上吧！会原谅，我的任性吗？",
        "对你们很失望。",
        "在对决时刻，我的心是一块石头。",
        "前往需要你们的地方。",
        "没有方向的河流，终会枯竭。",
        "哎呀，我可是吓的瑟瑟发抖呢，阁下。",
        "你的魔道不够纯粹。",
        "翻船哈哈哈。",
        "点亮的心，不会轻易熄灭。",
        "请原谅我的任性。",
        "守望着天空，大海和你的电梯。",
        "好好，干得不错。",
        "破碎的奇迹好过没有，苦恼的希望胜于迷惘。",
        "海边吹来的风，永远那么安宁。",
        "你们可真让人伤心。",
        "螳螂捕蝉，黄雀在后。",
        "演奏你的胡笳琴，或者，被胡笳琴所演奏。",
        "完美是最无情的禁锢。",
        "点亮的心不轻易熄灭。",
        "映照潮汐的起伏，以免迷失战场的倒影。",
        "前往需要你的地方。",
        "今天和大家过的一样普普通通。",
        "此时相望不相闻，愿逐月华流照君。鸿雁长飞光不度，鱼龙潜跃水成文。",
        "你看不见的眼里，隐藏着污秽。",
        "羡慕，因为是我想的模样。",
        "魔道的天才们属于同一种流派，偶像派。",
        "映照潮汐的起伏，以免迷失战场的道路。",
        "看不见的那只眼里，有你不该看见的过去。"
    ]
    index = random.randint(0, len(dicts))
    # 自动回复
    hash = soup.find('input', {"name": "formhash"})
    hash2 = hash.attrs['value']
    page = soup.find('input', {"name": "listextra"})
    page2 = page.attrs['value']
    fid = soup.find('input', {"name": "srhfid"})
    fid2 = fid.attrs['value']
    spl = str.split(url, '-')
    tid2 = spl[1]
    tagUrl = "http://108.170.5.74:8080/forum.php?mod=post&action=reply&fid=%s&tid=%s&extra=%s&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1" % (
        fid2, tid2, page2)
    logging.info(tagUrl)
    datax = {
        "message": dicts[index] + ' -- 发表于： ' + time.ctime(),
        "posttime": int(time.time()),
        "formhash": hash2,
        "usesig": "",
        "subject": ""
    }
    comment = session.post(tagUrl, datax, timeout=5)
    logging.info(datax)
    logging.info(comment.text)


# 检测目录
def mkdirx(name):
    current = os.getcwd()
    path = current + "/" + name
    if not os.path.exists(path):
        os.makedirs(name, 0o777)
    return path


# 下载单个图片
def downloadPic(url, path):
    # 获取文件名
    arr = str.split(url, "/")
    fileName = arr[-1]
    try:
        res = requests.get(url, timeout=2)
        img = res.content
        locFile = path + '/' + fileName
        logging.info(locFile)
        with open(locFile, 'wb') as f:
            f.write(img)
    except requests.exceptions.RequestException as e:
        logging.error(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    host = 'http://108.170.5.74:8080/'
    logging.basicConfig(level=logging.INFO)
    session = login(host)
    # getList(host, 'forum-18-1.html', session)
    path = 'http://108.170.5.74:8080/thread-1783265-1-1.html'
    getOne(host, path, session)
