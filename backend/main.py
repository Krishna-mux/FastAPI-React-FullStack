from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models import product
from backend.database import session, engine
import backend.database_models as database_models
from sqlalchemy.orm import Session 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def greet():
    return "welcome to our first fastAPI project"

# # crating an product by oops and using 
# products =[
#     product(1,'phn',22.2,10),
#     product(2,'charger',2.2,11),
#     product(3,'laptop',29.2,13),
# ]

products =[
    product(id=1, name= 'phn', price= 23, quantity= 12),
    product(id=23, name= 'phn-charger', price= 13, quantity= 10),
    product(id=32, name= 'phn-cover', price= 3, quantity= 2),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def inti_db():
    db = session()
    count = db.query(database_models.product).count()
    if count == 0:
        for product in products:
            db.add(database_models.product(**product.model_dump()))
        db.commit()
inti_db()


@app.get("/products")
def get_all_products( db : Session = Depends(get_db)):
    db_products = db.query(database_models.product).all()
    return db_products

@app.get('/products/{id}')
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        return db_product
    return "product Not Found" 
    # for product in products:
    #     if product.id == id:
    #         return product
    # return "Product Not found"


@app.post('/products')
def add_product(product: product, db:Session = Depends(get_db)):
    db.add(database_models.product(**product.model_dump()))
    db.commit()
    return product

## above code and below do same work but with different variable/parameter name..........
# @app.post('/product')
# def add_product(item: product):
#     products.append(item)
#     return item


@app.put('/products/{id}')
def update_product(id:int, product:product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        # db_product = product y not 
        db_product.name = product.name
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "updated!"
    else:
        return 'product not updated'


# @app.delete('/product')
# def delete_product(id:int):
#     for product in products:
#         if product.id == id:
#             products.remove(product)
#             return 'deleted'
#     return 'not deleted'

@app.delete('/products/{id}')
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        return 'not deleted'
    
    ## error facing while living the full stact project
# Access to XMLHttpRequest at 'http://localhost:8000/products/' from origin 'http://localhost:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
# :8000/products/:1  Failed to load resource: net::ERR_FAILED
# (index):1 Access to XMLHttpRequest at 'http://localhost:8000/products/' from origin 'http://localhost:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
# :8000/products/:1  Failed to load resource: net::ERR_FAILED