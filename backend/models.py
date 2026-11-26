from pydantic import BaseModel

class product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int 
# # crating an product by oops and using 

#     def __init__(self,id:int, name:str, price: float, quantity:int):
#         self.id = id
#         self.name = name
#         self.price = price
#         self.quantity = quantity

