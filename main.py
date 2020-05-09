import json
import os
import time
from pyquery import PyQuery as pq
import requests
import config
import headers
import secret
from model import Article, SQLModel
from utils import log, formatted_time, validate_title


# 构造获取文章列表需要访问的url
def article_list_url(begin, fakeid):
    query_string = dict(
        action='list_ex',
        begin=begin,
        count=5,
        fakeid=fakeid,
        type=9,
        query='',
        token=secret.token,
        lang='zh_CN',
        f='json',
        ajax=1,
    )
    url_prefix = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
    log('query', query_string)
    q = '&'.join(['{}={}'.format(k, v) for k, v in query_string.items()])
    url = url_prefix + '?' + q
    return url


# 获取列表里5期的所有文章的tag信息，并且存进数据库
def get_article_link(begin, publisher, fakeid):
    url = article_list_url(begin, fakeid)
    # 获取json响应
    r = requests.get(url, headers=headers.get_cookie())
    # json转化为字典
    d = json.loads(r.content)
    log('d', type(d), d)
    app_msg_list = d['app_msg_list']
    # log('app-msg-list', app_msg_list)
    articles = []
    # 查询条目是否已经在数据库中，不在则插入，存在则更新
    for item in app_msg_list:
        # 转义不能用在文件名里的非法字符
        item['title'] = validate_title(item['title'])
        # 文件名为时间+标题+html
        time_prefix = formatted_time(item['create_time']).split(' ', 1)[0].replace('/', '')
        item['filename'] = time_prefix + '-' + item['title']
        item['publisher'] = publisher
        a = Article.one(aid=item['aid'])
        if a is None:
            a = Article.new(item)
        else:
            a.update(a.id, **item)
            break

        articles.append(a)
        # 返回article对象的列表
    return articles


# 获取link，保存文章网页
def get(article):

    folder = os.path.join('archive', article.publisher)
    # 建立 archive 文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, article.filename + '.html')
    # 文件已存在则返回文件内容
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(article.link, headers=headers.get_cookie())
        with open(path, 'wb') as f:
            f.write(r.content)
            return r.content


# 获取图片的链接
def get_images_url(a):
    page = get(a)
    # css选择器拿到所有图片地址
    e = pq(page)
    images = e('img')
    images_url = []
    for i in images:
        ie = pq(i)
        url = ie.attr('data-src')
        # 去掉空的
        if url is not None:
            images_url.append(url)

    log('images', images_url)
    return images_url


# 图片已存在则不需要读取，不存在则写入
def save_img(urls, a):
    # 新建一个文件夹来存图，文件夹名是html文件的文件名
    # 文件夹不能和文件重名
    folder = os.path.join('archive', a.publisher, a.filename)
    log('folder', folder)
    if not os.path.exists(folder):
        os.makedirs(folder)

    # 用字典存储本地图片路径和网络路径的对应关系
    d = {}
    # 从传入的urls列表中的url下载图片，文件名为序号，左补零到2位
    for i in range(len(urls)):
        filename = '{:0>2d}.jpeg'.format(i)
        url = urls[i]
        path = os.path.join(folder, filename)
        if os.path.exists(path):
            pass
        else:
            # 发送网络请求, 把结果写入到文件夹中
            r = requests.get(url, headers=headers.get_cookie())
            with open(path, 'wb') as f:
                f.write(r.content)
        # 字典中填入本地图片的相对路径
        # src="filename\XX.jpeg"
        d[url] = path.split(os.sep, 2)[-1]
    return d


# 修改文件,将图片路径改为本地的路径
def update_file(d, article):
    folder = os.path.join( 'archive', article.publisher)
    path_old = os.path.join(folder, article.filename + '.html')
    path_new = os.path.join(folder, article.filename + '_bak.html')
    with open(path_old, encoding='utf-8') as f, open(path_new, 'w', encoding='utf-8') as fw:  # 打开两个文件，原始文件用来读，另一个文件将修改的内容写入
        for line in f:  # 遍历每行，取出来的是字符串，因此可以用replace 方法替换
            new_line = line.replace("data-src", "src")
            for k, v in d.items():
                new_line = new_line.replace(k, v)  # 逐行替换
            fw.write(new_line)  # 写入新文件
    os.remove(path_old)  # 删除原始文件
    os.rename(path_new, path_old)  # 修改新文件名， old -> new


if __name__ == '__main__':
    SQLModel.init_db()
    for publisher, fakeid in config.fakeid_lst.items():
        for i in range(config.number_of_pages):
            articles = get_article_link(i * 5, publisher, fakeid)
            for a in articles:
                urls = get_images_url(a)
                d = save_img(urls, a)
                update_file(d, a)
                time.sleep(1)
