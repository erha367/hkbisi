import requests, os, time, logging, re, random, yaml
from bs4 import BeautifulSoup

# 用户登录
def login():
    url = cfg["host"] + "member.php"
    querystring = {"mod": "logging", "action": "login", "loginsubmit": "yes", "infloat": "yes", "lssubmit": "yes",
                   "inajax": "1"}
    payload = "fastloginfield=username&username=%s&cookietime=2592000&password=%s&quickforward=yes" \
              "&handlekey=ls " % (cfg["name"], cfg["password"])
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "aae6a852-9f6c-2c0f-25dd-ac7b2ea2f7d0"
    }
    session2 = requests.session()
    res = session2.request("POST", url, data=payload, headers=headers, params=querystring)
    logging.info(res.text)
    return session2


# 列表页
def getList(url, session):
    res = session.get(host + url)
    soup = BeautifulSoup(res.text, 'html.parser')
    blocks = soup.find_all('a', class_='z')
    for b in blocks:
        url = cfg["host"] + b.attrs['href']
        # getOne(host, url, session)
        logging.info(url)


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
    dicts = cfg["comment"]
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
    tagUrl = cfg["host"] + "/forum.php?mod=post&action=reply&fid=%s&tid=%s&extra=%s&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1" % (
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
    path = "/Users/yangsen/pyshells/hkbisi/config.yaml"
    fs = open(path, encoding="UTF-8")
    cfg = yaml.load(fs, Loader=yaml.FullLoader)  # 添加后就不警告了
    fs.close()
    host = cfg['host']
    logging.basicConfig(level=logging.INFO)
    session = login()
    path = 'http://108.170.5.74:8080//thread-1891240-1-1.html'
    getOne(host, path, session)
