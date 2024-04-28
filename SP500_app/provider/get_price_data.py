from turtle import st
from app import db, api_key
from service.database_models import Stock
import asyncio
from aiohttp import ClientSession

base_url = 'https://paper-api.alpaca.markets'

async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()

async def update_stock_data(symbol, name, industry):
    stock = Stock.query.filter_by(symbol=symbol).first()
    if stock:
        stock.name = name
        stock.industry = industry
        db.session.commit()

async def get_stock_info():
    stocks = Stock.query.first()
    async with ClientSession() as session:
        tasks = []
        for stock in stocks:
            print (stock.symbol)
            url = f"{base_url}function=OVERVIEW&symbol={stock.symbol}&apikey={api_key}"
            task = asyncio.create_task(fetch_data(session, url))
            tasks.append(task)
            print(task)
        
        responses = await asyncio.gather(*tasks)
        
        update_tasks = []
        for stock, response in zip(stocks, responses):
            # Extract data fields from the response
            name = response.get('Name')
            industry = response.get('Industry')
            update_task = asyncio.create_task(update_stock_data(stock.symbol, name, industry))
            update_tasks.append(update_task)
        
        await asyncio.gather(*update_tasks)

# Execute the main function
if __name__ == "__main__":
    asyncio.run(get_stock_info())