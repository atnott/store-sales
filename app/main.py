from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .models import DB_NAME, Shop

app = FastAPI()
shop = Shop()

templates = Jinja2Templates(directory="app/templates")

@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
    products = shop.get_all_products()
    print(f"ТОВАРЫ ИЗ БАЗЫ: {products}")
    employees = shop.get_all_employees()

    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={"products": products, "employees": employees}
    )






