# -*- coding: UTF-8 -*-

from models import *
from fastapi import APIRouter
from service.walmart import WalmartApi
from utils import make_json_response


order_router = APIRouter()


@order_router.get('/order_list', summary='获取订单列表')
async def get_order(account_id: int,
                    nextCursor: Optional[str] = None,  #'下页标识'
                    sku: Optional[str] = None,  # ('', title='商品sku编码')
                    customerOrderId: Optional[str] = None,  # ('', title='客户订单编号')
                    purchaseOrderId: Optional[str] = None,  # ('', title='采购订单 ID。一位客户可能有多个采购订单')
                    status: Optional[str] = None,  # ('', title='采购订单行的状态。有效状态为：已创建、已确认、已发货、已交付和已取消')
                    createdStartDate: Optional[str] = None,  # ('', title='获取在此日期之后创建的所有采购订单。默认为当前日期 - 7 天')
                    createdEndDate: Optional[str] = None,  # ('', title='获取在此日期之前创建的所有采购订单')
                    fromExpectedShipDate: Optional[str] = None,  # ('', title='获取具有在此日期之后的预期发货日期的订单行的所有采购订单')
                    toExpectedShipDate: Optional[str] = None,  # ('', title='获取具有在此日期之前的预期发货日期的订单行的所有采购订单')
                    lastModifiedStartDate: Optional[str] = None,  # ('', title='获取在此日期之后修改的所有采购订单')
                    lastModifiedEndDate: Optional[str] = None,  # ('', title='获取在此日期之前修改的所有采购订单')
                    limit: Optional[str] = None,  # ('', title='每页要退回的订单数量')
                    productInfo: Optional[str] = None,  # ('', title='商品信息')
                    shipNodeType: Optional[str] = None,  # ('', title='船舶节点类型')
                    shippingProgramType: Optional[str] = None,  # ('', title='运输程序类型')
                    replacementInfo: Optional[str] = None,  # ('', title='替换信息')
                    orderType: Optional[str] = None,  # ('', title='订单类型')
):
    """返回订单列表"""
    result = await WalmartApi(account_id).get_order_list(nextCursor, sku, customerOrderId, purchaseOrderId, status,
                                                         createdStartDate, createdEndDate, fromExpectedShipDate,
                                                         toExpectedShipDate, lastModifiedStartDate, limit,
                                                         lastModifiedEndDate, productInfo, shipNodeType,
                                                         shippingProgramType, replacementInfo, orderType)
    return make_json_response(result)
