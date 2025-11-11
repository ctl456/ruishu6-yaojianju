"""HTTP请求服务模块"""
import os
import requests
from lxml import etree
from typing import Optional, Tuple
from utils.logger import log
from utils.file_handler import save_file, save_js_content
import config

def download_js_file(acw_tc: str, NfBCSins2OywS: str, NfBCSins2OywT: str | None,js_path: str, js_name: str) -> None:
    """
    下载外链JS文件

    Args:
        js_path: JS文件的相对路径
        js_name: 保存的文件名
    """
    cookies = {
        'acw_tc': acw_tc,
        'NfBCSins2OywS': NfBCSins2OywS,
    }
    if NfBCSins2OywT is not None:
        cookies['NfBCSins2OywT'] = NfBCSins2OywT

    response = requests.get(
        config.BASE_URL + js_path,
        headers=config.JS_REQUEST_HEADERS,
        cookies=cookies,
    )
    # 使用绝对路径保存
    file_path = os.path.join(config.JS_FILES_DIR, js_name)
    save_file(file_path, response.content, mode='wb')
    log.info(f'成功获取外链js: {js_path}')

def request_first_page() -> Tuple[str, str]:
    """
    第一次请求，获取初始cookie和JS文件

    Returns:
        NfBCSins2OywS cookie值
        acw_tc        cookie值
    """
    response = requests.get(
        config.TARGET_URL,
        headers=config.FIRST_REQUEST_HEADERS
    )

    html_text = etree.HTML(response.text)

    # 提取并保存content
    content = html_text.xpath('//meta[2]/@content')[0]
    save_js_content(
        os.path.join(config.JS_FILES_DIR, 'content.js'),
        content
    )

    # 保存script内容
    script = html_text.xpath('//head/script[1]/text()')[0]
    save_file(
        os.path.join(config.JS_FILES_DIR, 'ts.js'),
        script,
        mode='wb',
        encoding='utf-8'
    )
    log.info('成功获取script的js代码：ts.js')

    # 下载外链JS
    js_path = html_text.xpath('//head/script[2]/@src')[0]
    download_js_file(response.cookies['acw_tc'],response.cookies['NfBCSins2OywS'],None,js_path, "func.js")

    return response.cookies['acw_tc'], response.cookies['NfBCSins2OywS']


def verify_request(acw_tc: str, cookie_S: str, cookie_T: str) -> None:
    """
    验证请求，获取第二轮的JS文件

    Args:
        cookie_S: NfBCSins2OywS cookie值
        cookie_T: NfBCSins2OywT cookie值
    """
    cookies = {
        'acw_tc': acw_tc,
        'NfBCSins2OywS': cookie_S,
        'NfBCSins2OywT': cookie_T,
    }

    response = requests.get(
        config.TARGET_URL,
        cookies=cookies,
        headers=config.VERIFY_REQUEST_HEADERS,
    )

    # 保存HTML文件到js_files目录
    save_file(
        os.path.join(config.JS_FILES_DIR, "new.html"),
        response.content,
        mode='wb'
    )

    html_text = etree.HTML(response.text)

    # 提取并保存content
    content = html_text.xpath('//meta[5]/@content')[0]
    save_js_content(
        os.path.join(config.JS_FILES_DIR, 'content2.js'),
        content
    )

    # 保存script内容
    script = html_text.xpath('//head/script[1]/text()')[0]
    save_file(
        os.path.join(config.JS_FILES_DIR, 'ts2.js'),
        script,
        mode='wb',
        encoding='utf-8'
    )
    log.info('成功获取script中的js代码：ts2.js')

    # 下载外链JS
    js_path = html_text.xpath('//head/script[2]/@src')[0]
    download_js_file(acw_tc,cookie_S,cookie_T,js_path, "func2.js")


def fetch_data(acw_tc: str, cookie_S: str, cookie_T: str, _7QBHXKaZ: str, sign: str, timestamp: str, key_vaule: str, itemId: str) -> Optional[dict]:
    """
    获取最终数据

    Args:
        acw_tc:      acw_tc           cookie值
        cookie_S:    NfBCSins2OywS    cookie值
        cookie_T:    NfBCSins2OywT    cookie值
        _7QBHXKaZ:   7QBHXKaZ         参数
        sign:        sign             head
        timestamp:   timestamp        head
        key_vaule:   key_vaule        params
        itemId:      itemId           params

    Returns:
        API响应的JSON数据，如果失败返回None
    """
    cookies = {
        'enable_NfBCSins2Oyw': 'true',
        'acw_tc': acw_tc,
        'NfBCSins2OywS': cookie_S,
        'token': '',
        'STEP_TIPS_INDEX': 'true',
        'NfBCSins2OywT': cookie_T,
    }

    params = {
        'isSenior': 'N',
        'itemId': itemId,
        'pageNum': '1',
        'pageSize': '10',
        'searchValue': key_vaule,
        'timestamp': timestamp,
    }
    headers = config.API_REQUEST_HEADERS
    headers.update({'sign': sign, 'timestamp': timestamp})

    try:
        response = requests.get(
            config.API_URL,
            params=params,
            cookies=cookies,
            headers=headers,
        )

        log.info(f"响应状态码: {response.status_code}")
        log.info(f"响应内容: {response.text}")

        # 检查HTTP状态码
        response.raise_for_status()

        # 尝试解析JSON
        return response.json()

    except requests.exceptions.JSONDecodeError as e:
        log.error(f"JSON解析失败: {e}")
        log.error(f"原始响应内容: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        log.error(f"HTTP请求失败: {e}")
        return None
    except Exception as e:
        log.error(f"未知错误: {e}")
        return None