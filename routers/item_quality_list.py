# -*- coding: UTF-8 -*-

from models import *
from fastapi import APIRouter
from service.walmart import WalmartApi
from utils import make_json_response


item_quality_list_router = APIRouter()


@item_quality_list_router.post('/ItemQualityList', summary='获取商品质量信息详细数据')
async def get_item_quality_list(item: ItemQualityListModel,
                                limit: Optional[str] = None,
                                nextCursor: Optional[str] = None
                                ):
    result = await WalmartApi(item.account_id).get_item_quality_list(item.dict(), limit, nextCursor)
    return make_json_response(result)
