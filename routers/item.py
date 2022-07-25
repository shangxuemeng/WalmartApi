# -*- coding: UTF-8 -*-

from models import *
from fastapi import APIRouter
from service.walmart import WalmartApi
from utils import make_json_response


item_router = APIRouter()


@item_router.get('/items', summary='获取商品列表')
async def item_info(account_id: int,
                    nextCursor: Optional[str] = None,
                    offset: Optional[str] = None,
                    limit: Optional[str] = None,
                    sku: Optional[str] = None,
                    lifecycleStatus: Optional[str] = None,
                    publishedStatus: Optional[str] = None,
                    variantGroupId: Optional[str] = None
                    ):
    result = await WalmartApi(account_id).get_item_list(nextCursor, offset, limit, sku, lifecycleStatus,
                                                        publishedStatus, variantGroupId)
    return make_json_response(result)