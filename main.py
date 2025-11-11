import execjs
import time
from typing import Tuple
from services import request_first_page, verify_request, fetch_data
from utils import json_md5_to_str
from utils.logger import log

def get_cookie(js_path: str) -> str:
    with open(js_path,'r',encoding="utf-8") as f:
        js = f.read()
    ctx = execjs.compile(js)
    NfBCSins2OywT = ctx.call('get_cookie')
    NfBCSins2OywT = NfBCSins2OywT.split(';')[0]
    NfBCSins2OywT = NfBCSins2OywT.split('=')[1]
    return NfBCSins2OywT

def get_cookie_7QBHXKaZ(js_path: str, url: str) -> Tuple[str, str]:
    with open(js_path, 'r', encoding="utf-8") as f:
        js = f.read()
    ctx = execjs.compile(js)
    NfBCSins2OywT = ctx.call('get_cookie')
    NfBCSins2OywT = NfBCSins2OywT.split(';')[0]
    NfBCSins2OywT = NfBCSins2OywT.split('=')[1]
    _7QBHXKaZ = ctx.call('get_curr', url)
    _7QBHXKaZ = _7QBHXKaZ.split('7QBHXKaZ=')[1]
    return NfBCSins2OywT, _7QBHXKaZ


def main():
    """主流程"""
    # 第一步：获取初始cookie
    log.info("=" * 50)
    log.info("开始第一步：请求初始页面")
    log.info("=" * 50)
    acw_tc, cookie_S = request_first_page()
    log.info(f'成功获取 acw_tc: {acw_tc}')
    log.info(f'成功获取 NfBCSins2OywS: {cookie_S}')

    # 第二步：生成第一个cookie
    log.info("=" * 50)
    log.info("开始第二步：生成第一个cookie")
    log.info("=" * 50)
    cookie_T = get_cookie('./main.js')
    log.info(f'成功获取 NfBCSins2OywT: {cookie_T}')

    # 第三步：验证请求
    log.info("=" * 50)
    log.info("开始第三步：验证请求")
    log.info("=" * 50)
    verify_request(acw_tc, cookie_S, cookie_T)

    # 第四步：生成最终cookie和参数
    log.info("=" * 50)
    log.info("开始第四步：生成最终cookie和参数")
    log.info("=" * 50)
    cookie_T, _7QBHXKaZ = get_cookie_7QBHXKaZ('./main2.js','https://www.nmpa.gov.cn/datasearch/data/nmpadata/search')
    log.info(f'成功获取最终 NfBCSins2OywT: {cookie_T}')
    log.info(f'成功获取 7QBHXKaZ: {_7QBHXKaZ}')

    # 第五步：获取数据
    log.info("=" * 50)
    log.info("开始第五步：获取最终数据")
    log.info("=" * 50)
    searchValue = "阿司匹林"
    itemId = "ff80808183cad75001840881f848179f" # 从境内生产药品查询
    timestamp = str(int(round(time.time() * 1000)))
    sign = json_md5_to_str(itemId, searchValue, timestamp)
    result = fetch_data(acw_tc, cookie_S, cookie_T, _7QBHXKaZ, sign, timestamp, searchValue, itemId)

    log.info("=" * 50)
    log.info("流程完成！")
    log.info("=" * 50)

    return result

if __name__ == '__main__':
    main()