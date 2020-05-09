# 微信公众号文章爬虫

**简介**
-
- 基于 `requests` 库和 `pyquery` 。
- 可以批量爬取若干个微信公众号的文章，将`html`文本和图片分文件夹存储在本地，实现本地阅读。
- 基于 `pymysql` 实现了 `ORM`，存储文章信息。
- 实现了缓存，避免重复爬取。

**依赖**
-
- `Python 3.6`
- `MySQL`
- `requests`
- `pyquery`
- `PyMySQL`

**如何运行**
-
- 首先需要登录[微信公众平台](https://mp.weixin.qq.com)，如果没有公众号请注册一个。
- 登录之后，在左侧边菜单点击 `素材管理`， 再在刷新出的页面点击 `新建图文消息`， 再点击上方的 `超链接`， 
在弹出的浮窗中点击 `选择其他公众号`，输入你想要爬取的公众号名称并按回车搜索。
- 按 `F12`， 点击 `Network` 选项卡。在公众号文章链接浮窗那里翻页，查看浏览器抓包。
复制保存 `Request Headers` 的 `Cookie` 字段和 `Query String Parameters` 的 `token` 和 `fakeid` 字段。
- 您需要在根目录下添加 `secret.py` 文件，内容为：
    ```python
    mysql_password = '您的 MySQL 密码'
    token = '您保存的token'
    cookie = '您在上一步保存的 Cookie'
    ```
- 您需要在 `config.py` 中输入一些配置信息
    ```python
    db_name = '想取的数据库名'
    number_of_pages = 想要爬取的页数，每页包含5次推送
    fakeid_lst = {
    '公众号名称': '您在之前保存的该公众号的fakeid',
    '另一个公众号': '另一个fakeid',
    }
    ```
- 运行 `db_reset.py`

- 运行 `main.py`
- 爬取的文章和图片保存在项目根目录下的 `archive` 文件夹中，按不同公众号分文件夹保存，
`html` 文件名为 ‘发布时间-文章标题’。
打开 `html` 文件即可本地阅读文章。
- 注意 `Cookie` 和 `token` 是会失效的，下一次爬取之前，需要在文件中更新这两项内容。