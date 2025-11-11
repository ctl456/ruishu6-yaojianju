"""Cookie解析工具模块"""


def parse_cookie_value(cookie_full: str) -> str:
    """
    从完整的cookie字符串中提取值

    Args:
        cookie_full: 完整的cookie字符串，格式如 "name=value; path=/"

    Returns:
        提取出的cookie值
    """
    if '=' in cookie_full:
        cookie_value = cookie_full.split('=', 1)[1]
    else:
        cookie_value = cookie_full

    return cookie_value.split(';')[0]