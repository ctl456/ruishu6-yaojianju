import os

# ===== 路径配置 =====
# 获取config.py所在目录（项目根目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# JS文件保存目录
JS_FILES_DIR = BASE_DIR

# 确保目录存在
os.makedirs(JS_FILES_DIR, exist_ok=True)

# ===== URL配置 =====
BASE_URL = 'https://www.nmpa.gov.cn'
TARGET_URL = f'{BASE_URL}/datasearch/home-index.html'
API_URL = f'{BASE_URL}/datasearch/data/nmpadata/search'

# ===== Headers配置 =====
# 第一次请求的headers
FIRST_REQUEST_HEADERS = {
    'Host': 'www.nmpa.gov.cn',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# 获取JS文件的headers
JS_REQUEST_HEADERS = {
    'Host': 'www.nmpa.gov.cn',
    'sec-ch-ua-platform': '"Windows"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script',
    'Referer': 'https://www.nmpa.gov.cn/datasearch/home-index.html',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# 验证请求的headers
VERIFY_REQUEST_HEADERS = {
    'Host': 'www.nmpa.gov.cn',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.nmpa.gov.cn/datasearch/home-index.html',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# API请求的headers
API_REQUEST_HEADERS = {
    'Host': 'www.nmpa.gov.cn',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'token': 'false',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.nmpa.gov.cn/datasearch/search-result.html',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
