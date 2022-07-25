# -*- coding: UTF-8 -*-
from typing import Optional, List
from pydantic import BaseModel, Field


class WalmartModel(BaseModel):
    account_id: int = Field(title="account_id")


class QueryModel(BaseModel):
    """
    title	Product Title
    sku	An arbitrary alphanumeric unique ID, seller-specified, identifying each item
    itemId	Specifies the item identifier generated by Walmart
    """
    field: Optional[str] = Field(title='Enum: "title" "sku" "itemId"')
    value: Optional[str] = None


class ItemFilterModel(BaseModel):
    field: Optional[str] = Field(title='Enum: "contentDiscoverabilityPercentage", "qualityScorePercentage" '
                                       '"offerPercentage" "ratingReviewsPercentage" "viewTrendingItems" '
                                       '"viewPostPurchaseItems" "wfsFlag" "categoryName" "hasIssues" "productType" '
                                       '"attributeList" "productTypes" "brandList" "oos" "fastAndFreeShipping" '
                                       '"priceMeetBeatFlag"')
    op: Optional[str] = Field(title='Enum: "equals" "between"')
    values: List[int] = []


class BodyModel(BaseModel):
    # limit: Optional[str] = None
    # nextCursor: Optional[str] = None
    query: QueryModel
    ItemFilterList: List[ItemFilterModel]


class ItemQualityListModel(WalmartModel):
    """获取商品列表质量评分"""
    body: BodyModel







