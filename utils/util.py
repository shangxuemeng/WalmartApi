# coding=utf-8

import orjson
from .log import logger
from copy import deepcopy
from fastapi.responses import JSONResponse
import zipfile, tempfile, csv
import os


def make_json_response(data, status_code=200):
    return JSONResponse(content={
        "success": True,
        "msg": "",
        "data": data
    }, status_code=status_code)


def data_to_json(data):
    json_data = None
    try:
        json_data = orjson.loads(data)
    except Exception as e:
        logger.error(e, exc_info=e)
    return json_data


def gdict(d, key_str, default=None, str_split="/", or_split="|", expression_split="!", **kwargs):
    _ = deepcopy(d)
    _dict = deepcopy(d)
    flag = None
    for exp in key_str.split(expression_split):
        for key in exp.split(str_split):
            flag = False
            for k in key.split(or_split):
                temp_dict = _dict.get(k)
                if temp_dict or temp_dict == 0:
                    _dict = temp_dict
                    flag = True
                    break
            if not flag:
                break
        if flag:
            return _dict
        _dict = _
    return default


def read_csv_file(resp):
    file_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'media')
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    # try:
    _tmp_file = tempfile.TemporaryFile()  # 创建临时文件
    _tmp_file.write(resp.content)  # byte字节数据写入临时文件

    zf = zipfile.ZipFile(_tmp_file, mode='r')
    for names in zf.namelist():
        zf.extract(names, file_path)  # 解压到指定目录文件下
    zf.close()
    with open(os.path.join(file_path, names), 'r', encoding='utf-8') as f:
        resder = csv.reader(f)
        filenames = next(resder)  # 获取数据的第一列，作为后续要转为字典的键名 生成器，next方法获取
        csv_reader = csv.DictReader(f, fieldnames=filenames)
        data_list = []
        for row in csv_reader:
            d = {}
            for k, v in row.items():
                d[k] = v
            data_list.append(d)
        f.close()
        new_dict = {'data_list': data_list}
    del_file(file_path)

    return new_dict


def del_file(file_path):
    """
    下载完成后删除文件
    :param file_path: 文件路径
    :return:
    """
    # 文件路径
    for root, dirs, files in os.walk(file_path):
        for name in files:
            if name.endswith(".csv"):  # 填写规则
                os.remove(os.path.join(root, name))
                logger.info("Delete File: " + os.path.join(root, name))
