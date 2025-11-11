import hashlib
import urllib.parse

def json_md5_to_str(itemId: str, searchValue: str, timestamp: str) -> str:
    """
    实现了与提供的JavaScript代码等效的加密逻辑。

    Args:
        params (str): 待加密的URL参数字符串。
        app_secret (str): 用于签名的密钥。

    Returns:
        str: 计算出的32位小写MD5哈希值。
    """
    # 步骤 1: 将原始参数字符串、'&'符号和appSecret密钥拼接在一起
    # 这对应 JavaScript 中的 case '5'
    params = "isSenior=N&itemId=" + itemId + "&pageNum=1&pageSize=10&searchValue=" + searchValue + "&timestamp=" + timestamp
    app_secret = "nmpasecret2020"

    combined_string = f"{params}&{app_secret}"

    # 步骤 2: 对拼接后的完整字符串进行URL编码
    # Python的 urllib.parse.quote(..., safe='') 的行为等同于
    # JavaScript的 encodeURIComponent 再加上对 '!', '(', ')', '~' 等特殊字符的手动替换。
    # 因此，这一步就完成了JS中的 case 3, 1, 2, 0, 6 的所有工作。
    # safe='' 参数确保了所有保留字符（除了 - _ .）都被编码，与JS逻辑保持一致。
    encoded_string = urllib.parse.quote(combined_string, safe='')

    # 步骤 3: 对最终处理好的字符串进行MD5加密
    # 这对应 JavaScript 中的 case '4'
    # a. 将字符串编码为bytes (MD5算法需要bytes类型输入)，通常使用utf-8
    string_bytes = encoded_string.encode('utf-8')

    # b. 创建MD5对象并计算哈希值
    md5_hash = hashlib.md5(string_bytes)

    # c. 获取16进制表示的摘要 (32位小写)，即最终结果
    hex_digest = md5_hash.hexdigest()

    return hex_digest