from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import os
from .db import Database
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Xianyu Custom - Minimal Backend")

# serve frontend static files at /frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

DB = Database('./data/app.db')

class Account(BaseModel):
    id: Optional[int]
    name: str
    cookie: Optional[str] = None
    enabled: bool = True

class Product(BaseModel):
    id: Optional[int]
    title: str
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    images: Optional[List[str]] = []
    spec: Optional[str] = None

class Material(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str] = None
    images: Optional[List[str]] = []

@app.on_event("startup")
def startup_event():
    DB.create_tables()

@app.get('/health')
def health():
    return {"status": "ok"}

# Accounts
@app.get('/accounts', response_model=List[Account])
def list_accounts():
    return DB.list_accounts()

@app.post('/accounts', response_model=Account)
def add_account(a: Account):
    aid = DB.add_account(a.name, a.cookie, a.enabled)
    a.id = aid
    return a

@app.delete('/accounts/{account_id}')
def delete_account(account_id: int):
    DB.delete_account(account_id)
    return {"deleted": account_id}

# Products
@app.get('/products', response_model=List[Product])
def list_products():
    return DB.list_products()

@app.post('/products', response_model=Product)
def add_product(p: Product):
    pid = DB.add_product(p.title, p.category, p.description, p.price, p.original_price, p.images, p.spec)
    p.id = pid
    return p

@app.put('/products/{product_id}', response_model=Product)
def update_product(product_id: int, p: Product):
    DB.update_product(product_id, p.title, p.category, p.description, p.price, p.original_price, p.images, p.spec)
    p.id = product_id
    return p

@app.post('/products/{product_id}/upload-image')
def upload_image(product_id: int, file: UploadFile = File(...)):
    os.makedirs('data/images', exist_ok=True)
    filename = file.filename
    safe_name = filename.replace(' ', '_')
    path = f"data/images/{product_id}_{safe_name}"
    with open(path, 'wb') as f:
        f.write(file.file.read())
    DB.add_image_to_product(product_id, path)
    return {"path": path}

# Materials (素材库)
@app.get('/materials', response_model=List[Material])
def list_materials():
    return DB.list_materials()

@app.post('/materials', response_model=Material)
def add_material(m: Material):
    mid = DB.add_material(m.title, m.description, m.images)
    m.id = mid
    return m

@app.delete('/materials/{material_id}')
def delete_material(material_id: int):
    DB.delete_material(material_id)
    return {"deleted": material_id}

@app.post('/materials/{material_id}/upload-image')
def upload_material_image(material_id: int, file: UploadFile = File(...)):
    os.makedirs('data/materials', exist_ok=True)
    filename = file.filename
    safe_name = filename.replace(' ', '_')
    path = f"data/materials/{material_id}_{safe_name}"
    with open(path, 'wb') as f:
        f.write(file.file.read())
    DB.add_material_image(material_id, path)
    return {"path": path}

# Attribute recognition (mock)
@app.post('/recognize-attributes')
def recognize_attributes(title: str = Form(...), description: str = Form(None)):
    # Placeholder: simple keyword-based recognition
    suggested_category = None
    title_lower = title.lower()
    if any(k in title_lower for k in ['手机', '耳机', '电脑', 'iphone', 'oppo', '小米']):
        suggested_category = '数码配件'
    elif any(k in title_lower for k in ['书', '教材', '课程']):
        suggested_category = '书籍'
    else:
        suggested_category = '其他'

    # spec extraction naive
    suggested_spec = None
    if 'N1' in title or 'N2' in title:
        suggested_spec = '等级证书'

    return {"category": suggested_category, "spec": suggested_spec}

# Batch publish (simulate)
class PublishRequest(BaseModel):
    product_ids: List[int]
    account_ids: List[int]

@app.post('/publish')
def publish(req: PublishRequest):
    recs = []
    for pid in req.product_ids:
        for aid in req.account_ids:
            rec = DB.add_publish_record(aid, pid)
            recs.append({"account_id": aid, "product_id": pid, "record_id": rec})
    return {"published": recs}

@app.get('/publish-records')
def publish_records():
    return DB.list_publish_records()
