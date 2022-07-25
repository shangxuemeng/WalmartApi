# coding=utf-8

import asyncio
from .util import data_to_json, read_csv_file
from error import RequestError
from httpx import AsyncClient, Timeout


async def request(method, url, headers=None, params=None, data=None, json_data=None, resp_to_json=True):
    retry = 5
    exc = None
    while retry:
        try:
            async with AsyncClient(headers=headers, timeout=Timeout(30), http2=True) as session:
                resp = await session.request(method, url, params=params, data=data, json=json_data)
                body = await resp.aread()
                if resp_to_json:
                    body = data_to_json(body)
                return body
        except Exception as _exc:
            exc = _exc
            retry -= 1
            await asyncio.sleep(0.5)
    raise RequestError(url, exc)


async def request_str(method, url, headers=None, params=None, data=None, json_data=None, resp_to_json=True):
    retry = 5
    exc = None
    while retry:
        try:
            async with AsyncClient(headers=headers, timeout=Timeout(30), http2=True) as session:
                resp = await session.request(method, url, params=params, data=data, json=json_data)
                new_dict = read_csv_file(resp)
                if resp_to_json:
                    return new_dict
        except Exception as _exc:
            exc = _exc
            retry -= 1
            await asyncio.sleep(0.5)
    raise RequestError(url, exc)

