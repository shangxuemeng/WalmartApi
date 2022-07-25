# -*- coding: UTF-8 -*-

from models import *
from fastapi import APIRouter, Query
from service.walmart import WalmartApi
from utils import make_json_response


report_router = APIRouter()

"""
   “promo”：促销报告
   “returnOverrides”：退货商品覆盖报告
   “buybox”：buy box报告
   “cpa”：cpa报告
   “itemPerformance”：商品绩效报告  "version": 2
"""


@report_router.get('/report', summary='返回各类型报告数据')
async def get_report(account_id: int,
                     type: str = Query(..., title='报告类型参数'),
                     version: Optional[str] = None):
    """返回各类型报告"""
    result = await WalmartApi(account_id).get_report(type, version)
    return make_json_response(result)
