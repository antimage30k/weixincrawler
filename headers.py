
'''带上从浏览器里复制过来的user-agent和cookie'''
import secret


def get_cookie():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.110 '
                      'Safari/537.36',
        'Cookie': secret.cookie,
    }

    return headers

