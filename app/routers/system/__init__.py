from app.routers.system import stock_data, index_data

routers = [
    stock_data.router,
    index_data.router
]