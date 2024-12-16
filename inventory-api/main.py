from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-13713.c57.us-east-1-4.ec2.redns.redis-cloud.com",
    port=13713,
    password="fXZkEaDFkPX9chd5bp15u3n3PlAUJDHy",
    decode_responses=True
)

# Pydantic model for Product
class ProductIn(BaseModel):
    name: str
    price: float
    quantity: int

# Redis OM model for Product
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

    class Config:
        arbitrary_types_allowed = True


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()] #may also use directly Product.get(pk) here

def format(pk: str):
    product = Product.get(pk)

    return{
        'id':product.pk,
        'name':product.name,
        'price':product.price,
        'quantity':product.quantity
    }



@app.post('/products')
def create(product: ProductIn):  # Using Pydantic model here
    p = Product(**product.dict())  # Convert to Redis OM model
    p.save()
    return p

@app.get('/products/{pk}')
def get(pk:str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk:str):
    return Product.delete(pk)

