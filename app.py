# -*- coding: UTF-8 -*-

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import item_router, report_router
from routers.date import date_router
from routers.inventory import inventory_router
from routers.item_quality_list import item_quality_list_router
from routers.order import order_router
from routers.over_item_quality import over_item_quality_router
from routers.reconciliation import reconciliation_router
from routers.item_quality_count import item_quality_count_router

import nest_asyncio

nest_asyncio.apply()

app = FastAPI()


@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    return JSONResponse(status_code=500, content={
        'success': False,
        'msg': f'failed to execute: {request.method}: {request.url}, Error: {err}',
        'data': None
    })

app.include_router(item_router)
app.include_router(order_router)
app.include_router(inventory_router)

app.include_router(report_router)
app.include_router(date_router)
app.include_router(reconciliation_router)
app.include_router(over_item_quality_router)
app.include_router(item_quality_list_router)
app.include_router(item_quality_count_router)


if __name__ == '__main__':
    uvicorn.run(app)
