# -*- coding: UTF-8 -*-

from fastapi import APIRouter, Query
from service.walmart import WalmartApi
from utils import make_json_response


over_item_quality_router = APIRouter()


@over_item_quality_router.get('/OverItemQuality', summary="获取卖家整体商品质量")
async def get_over_item_quality(account_id: int,
                                viewTrendingItems: bool = Query(None),
                                wfsFlag: str = Query(None)
):
    result = await WalmartApi(account_id).get_over_item_quality(viewTrendingItems, wfsFlag)
    return make_json_response(result)
