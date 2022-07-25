# -*- coding: UTF-8 -*-

from models import *
from fastapi import APIRouter, Query
from service.walmart import WalmartApi
from utils import make_json_response


inventory_router = APIRouter()


@inventory_router.get('/inventory', summary='获取指定商品库存')
async def inventory_info(account_id: int,
                         sku: str = Query(..., title='商品skuid'),
                         shipNode: Optional[str] = None):
    result = await WalmartApi(account_id).get_inventory_info(sku, shipNode)
    return make_json_response(result)
