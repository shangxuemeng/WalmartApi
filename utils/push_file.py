# -*- coding: utf-8 -*-
# flake8: noqa
import os
import time
import threading
from urllib.parse import quote
from qiniu import Auth, put_file, etag, put_data, put_stream
from qiniu.config import set_default
try:
    from .day_log import log_set
except ImportError:
    def log_set(message, *args, **kwargs):
        print(message)

# 不显示上传信息
INFO_SHOW = True

# 需要填写你的 Access Key 和 Secret Key
access_key = 'QSvtvN4Ons1CiNzaMGqx8XmDaiM1L0ZqSwJ2YoTn'
secret_key = 'yagRd-cBOVhkRGGT-o_reMqNVjI8_k7YwoTXkhrm'
# 要上传的空间
bucket_name = 'bailun-publish-img'


def set_info_show_flag(flag: bool):
    """
    设置上传信息是否展示
    """
    global INFO_SHOW
    INFO_SHOW = flag


def _make_key(filename='', file_path='', unique=False):
    """制作key"""
    # assert any((
        #(filename and os.path.isfile(filename)),
        #(file_path and os.path.isfile(file_path))
    # ))
    assert any((filename, file_path)), "非法文件路径"
    # 上传后保存的文件名
    if filename:
        key = filename
        file_path = filename
    else:
        _, key = os.path.split(file_path)
    if unique:
        _end_, *_head_ = key[::-1].split('.', 1)
        if _head_:
            key = _head_[0][::-1] + '_' + str(int(time.time())) + '.' + _end_[::-1]
        else:
            key = _end_[::-1] + '_' + str(int(time.time()))
    return key


def make_url(key: str):
    """制作文件名"""
    # 强转为url编码
    key = quote(key)
    return 'http://img.blsct.com/' + key + '?v={}'.format(int(time.time()))


def _push_file(key: str, file_path: str, timeout=0):
    """上传文件逻辑"""
    # 设置超时
    if timeout:
        set_default(connection_timeout=timeout)
    for i in range(3):
        try:
            # 构建鉴权对象
            q = Auth(access_key, secret_key)
            # 生成上传 Token，可以指定过期时间等
            token = q.upload_token(bucket_name, key, 60 * 60 * 24 * 2)
            if INFO_SHOW:
                log_set('开始上传文件', 'INFO')
            t = time.time()
            # ret, info = put_data(token, key, data)
            # ret, info = put_file(token, key, file_path)
            f = open(file_path, 'rb')
            size = os.path.getsize(file_path)
            ret, info = put_stream(token, key, f, file_path, size)
            f.close()
            if not ret:
                if INFO_SHOW:
                    log_set(info.error, 'INFO')
                    log_set('上传失败', 'INFO')
                return ''
            else:
                if INFO_SHOW:
                    log_set(ret['key'], 'INFO')
                    log_set(f'上传成功,耗时{time.time() - t:.3f}秒', 'INFO')
                # assert ret['key'] == key
                # assert ret['hash'] == etag(localfile)
                return make_url(key)
        except Exception as e:
            if i < 2:
                time.sleep(3)
                if INFO_SHOW:
                    log_set(f'上传失败，重试第{i+1}遍', 'WARING')
                continue
            else:
                raise e


def push_file(filename='', file_path='', timeout=0, unique=False):
    """
    阻塞上传图片，在完成后返回文件url
    :filename 文件名（当前目录,优先于filename）
    :file_path 文件绝对路径（与filename相斥）
    :timeout 上传超时（0是默认自动则是30秒）
    :unique 唯一，且不覆盖
    """
    key = _make_key(filename, file_path, unique)
    return _push_file(key, filename if filename else file_path, timeout)


def await_push_file(filename='', file_path='', timeout=0, unique=False):
    """
    异步上传文件，优先返回文件url，再在后续中上传文件。不在乎上传文件的成结果
    :filename 文件名（当前目录）
    :file_path 文件绝对路径（与filename相斥）
    :timeout 上传超时（0是默认自动则是30秒）
    :unique 唯一，且不覆盖
    """
    key = _make_key(filename, file_path, unique)
    url = make_url(key)
    t = threading.Thread(target=_push_file, args=(key, filename if filename else file_path, timeout))
    t.start()
    return url


if __name__ == '__main__':
    # res = push_file(file_path=r"C:\Users\Administrator\Desktop\s-l225.jpg")
    # res = await_push_file(file_path=r"C:\Users\Administrator\Desktop\s-l225.jpg")
    res = await_push_file(file_path=r"F:\jpg\ex2\_bak\E_UsmE4VgAU53Ub.jpg")
    print(res)
