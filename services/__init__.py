"""服务模块初始化"""
from .request_service import (
    download_js_file,
    request_first_page,
    verify_request,
    fetch_data
)

__all__ = [
    'download_js_file',
    'request_first_page',
    'verify_request',
    'fetch_data',
]