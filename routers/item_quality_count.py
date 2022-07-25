# -*- coding: UTF-8 -*-

from models import *
from fastapi import APIRouter
from service.walmart import WalmartApi
from utils import make_json_response


item_quality_count_router = APIRouter()


@item_quality_count_router.get('/ItemQualityCount', summary="获取商品质量计数")
async def get_item_quality_count(account_id: int,
                                viewTrendingItems: Optional[bool] = None,
                                wfsFlag: Optional[bool] = None,
                                hasIssue: Optional[int] = None,
                                type: Optional[str] = None,
                                limit: Optional[int] = None,
                                offset: Optional[int] = None
):
    result = await WalmartApi(account_id).get_item_quality_count(
        viewTrendingItems, wfsFlag, hasIssue, type, limit, offset)
    return make_json_response(result)
