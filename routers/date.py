# -*- coding: UTF-8 -*-

from models import *
from fastapi import APIRouter
from service.walmart import WalmartApi
from utils import make_json_response


date_router = APIRouter()


@date_router.get('/date_list', summary='获取对账报告数据指定日期列表')
async def date_list(account_id: int):
    """返回对账报告可用的日期列表"""
    result = await WalmartApi(account_id).get_report_date()
    return make_json_response(result)
