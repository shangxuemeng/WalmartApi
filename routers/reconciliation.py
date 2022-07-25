# -*- coding: UTF-8 -*-

from models import *
from fastapi import APIRouter, Query
from service.walmart import WalmartApi
from utils import make_json_response


reconciliation_router = APIRouter()


@reconciliation_router.get('/reconciliation', summary='获取指定日期的对账报告数据')
async def reconciliation_report(account_id: int,
                                reportDate: str = Query(..., title='对账报告日期')):
    """返回指定日期的对账报告"""
    result = await WalmartApi(account_id).get_reconciliation_report(reportDate)
    return make_json_response(result)
