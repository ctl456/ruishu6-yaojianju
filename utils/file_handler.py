"""文件读写操作模块"""
import json
import os
from .logger import log

def ensure_dir(file_path: str) -> None:
    """确保文件所在目录存在"""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        log.info(f'创建目录: {directory}')

def save_file(filename: str, content, mode: str = 'w', encoding: str = 'utf-8') -> None:
    """
    保存文件

    Args:
        filename: 文件路径
        content: 文件内容（str或bytes）
        mode: 写入模式
        encoding: 编码格式
    """
    # 确保目录存在
    ensure_dir(filename)

    write_mode = 'wb' if 'b' in mode else 'w'

    if write_mode == 'wb':
        content = content.encode(encoding) if isinstance(content, str) else content

    with open(filename, write_mode) as f:
        f.write(content)

    log.info(f'成功保存文件: {filename}')

def read_file(filename: str, encoding: str = 'utf-8') -> str:
    """
    读取文件

    Args:
        filename: 文件路径
        encoding: 编码格式

    Returns:
        文件内容
    """
    if not os.path.exists(filename):
        log.error(f'文件不存在: {filename}')
        raise FileNotFoundError(f'文件不存在: {filename}')

    with open(filename, 'r', encoding=encoding) as f:
        return f.read()

def save_js_content(filename: str, content: str) -> None:
    """
    保存JS内容为字符串格式

    Args:
        filename: 文件路径
        content: JS内容
    """
    content_str = 'content = ' + json.dumps(content) + ';'
    # 只在日志中显示前100个字符
    preview = content_str[:100] + '...' if len(content_str) > 100 else content_str
    log.info(f'准备保存JS内容: {preview}')
    save_file(filename, content_str, mode='wb', encoding='utf-8')