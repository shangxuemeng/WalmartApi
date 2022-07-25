# -*- coding: UTF-8 -*-

from utils.request import request, request_str
from utils.account import Account, AccountError
from uuid import uuid4
import base64
from utils.log import logger


class WalmartApi:

    def __init__(self, account_id: int = None):
        self.account_id = account_id
        self.client_id = None
        self.client_secret = None
        self.headers = {"Authorization": ""}
        self.base_url = 'https://marketplace.walmartapis.com'


    @classmethod
    def parse_params(cls, params: dict):
        return dict(filter(lambda x: x[1], list(zip(params.keys(), params.values()))))

    async def _init_account(self):
        account_info = await Account.get_account(self.account_id)
        self.client_id = account_info["client_id"]
        self.client_secret = account_info["client_secret"]
        self.data = bytes(self.client_id + ':' + self.client_secret, "utf-8")
        self.auth = base64.b64encode(self.data).decode("ascii")
        self.headers["Authorization"] = 'Basic %s' % self.auth
        self.headers['WM_QOS.CORRELATION_ID'] = str(uuid4())
        self.headers['WM_SVC.NAME'] = 'Walmart Marketplace'
        self.headers['Accept'] = 'application/json'

    async def get_token(self):
        url = 'https://marketplace.walmartapis.com/v3/token'
        try:
            json_data = await request("POST", headers=self.headers, url=url, data={"grant_type": 'client_credentials'})
            if json_data.get("access_token"):
                return json_data['access_token']
        except Exception as e:
            logger.error(e, exc_info=e)
        raise AccountError(self.account_id)

    # 获取商品列表
    async def get_item_list(self, nextCursor, offset, limit, sku, lifecycleStatus, publishedStatus,
                            variantGroupId):
        await self._init_account()
        self.headers['WM_SEC.ACCESS_TOKEN'] = await self.get_token()
        url = self.base_url + '/v3/items'
        params = self.parse_params({
            "nextCursor": nextCursor,
            "offset": offset,
            "limit": limit,
            "sku": sku,
            "lifecycleStatus": lifecycleStatus,
            "publishedStatus": publishedStatus,
            "variantGroupId": variantGroupId
        })
        return await request("GET", url, headers=self.headers, params=params)

    # 订单列表获取
    async def get_order_list(self, nextCursor, sku, customerOrderId, purchaseOrderId, status,
                                                         createdStartDate, createdEndDate, fromExpectedShipDate,
                                                         toExpectedShipDate, lastModifiedStartDate, limit,
                                                         lastModifiedEndDate, productInfo, shipNodeType,
                                                         shippingProgramType, replacementInfo, orderType):
        await self._init_account()
        self.headers['WM_SEC.ACCESS_TOKEN'] = await self.get_token()
        url = self.base_url + '/v3/orders'
        params = self.parse_params({
            "nextCursor": nextCursor,
            "sku": sku,
            "customerOrderId": customerOrderId,
            "limit": limit,
            "purchaseOrderId": purchaseOrderId,
            "status": status,
            "createdStartDate": createdStartDate,
            "createdEndDate": createdEndDate,
            "fromExpectedShipDate": fromExpectedShipDate,
            "toExpectedShipDate": toExpectedShipDate,
            "lastModifiedStartDate": lastModifiedStartDate,
            "lastModifiedEndDate": lastModifiedEndDate,
            "productInfo": productInfo,
            "shipNodeType": shipNodeType,
            "shippingProgramType": shippingProgramType,
            "replacementInfo": replacementInfo,
            "orderType": orderType,
        })
        return await request("GET", url, headers=self.headers, params=params)

    # 获取指定商品的库存
    async def get_inventory_info(self, sku, shipNode):
        await self._init_account()
        self.headers['WM_SEC.ACCESS_TOKEN'] = await self.get_token()
        url = self.base_url + '/v3/inventory'
        params = self.parse_params({
            "sku": sku,
            "shipNode": shipNode,
        })
        return await request("GET", url, headers=self.headers, params=params)

    # 获取报告
    async def get_report(self, type, version):
        await self._init_account()
        self.headers['WM_SEC.ACCESS_TOKEN'] = await self.get_token()
        url = self.base_url + '/v3/getReport'
        params = self.parse_params({
            "type": type,
            "version": version,
        })
        return await request_str("GET", url, headers=self.headers, params=params)

    # 获取报告日期
    async def get_report_date(self):
        await self._init_account()
        self.headers['WM_SEC.ACCESS_TOKEN'] = await self.get_token()
        url = self.base_url + '/v3/report/reconreport/availableReconFiles'
        return await request("GET", url, headers=self.headers)

    # 获取对账报告数据
    async def get_reconciliation_report(self, report_date):
        await self._init_account()
        self.headers['WM_SEC.ACCESS_TOKEN'] = await self.get_token()
        url = self.base_url + '/v3/report/reconreport/reconFile'
        params = self.parse_params({
            "reportDate": report_date,
        })
        return await request_str("GET", url, headers=self.headers, params=params)

    # 获取卖家整体商品质量
    async def get_over_item_quality(self, viewTrendingItems, wfsFlag):
        await self._init_account()
        self.headers['WM_SEC.ACCESS_TOKEN'] = await self.get_token()
        url = self.base_url + '/v3/insights/items/listingQuality/score'
        params = {
            "viewTrendingItems": viewTrendingItems,
            "wfs_flag": wfsFlag,
        }
        return await request("GET", url, headers=self.headers, params=params)

    # 获取商品列表质量详细信息
    async def get_item_quality_list(self, body, limit, nextCursor):
        await self._init_account()
        self.headers['WM_SEC.ACCESS_TOKEN'] = await self.get_token()
        url = self.base_url + '/v3/insights/items/listingQuality/items'
        par = self.parse_params(
            {'limit': limit,
             'nextCursor': nextCursor
             }
        )
        return await request("POST", url, headers=self.headers, params=par, json_data=body)

    async def get_item_quality_count(self, viewTrendingItems, wfsFlag, hasIssue, type, limit, offset):
        await self._init_account()
        self.headers['WM_SEC.ACCESS_TOKEN'] = await self.get_token()
        url = self.base_url + '/v3/insights/items/listingQuality/count'
        pars = self.parse_params({
            'viewTrendingItems': viewTrendingItems,
            'wfsFlag': wfsFlag,
            'hasIssue': hasIssue,
            'type': type,
            'limit': limit,
            'offset': offset,
        })
        return await request("GET", url, headers=self.headers, params=pars)
