برای یک کتابخانه سبک جهت مدیریت پایگاه داده با استفاده از Sqlalchemy برای استفاده در فایل README.md گیتهاب به انگلیسی معرفی بنویس و به صورت فایل ارسال کن

اسم کتابخانه Dabas است

برای فراخوانی :
from Dabas import DatabaseManager, SessionFactory


برای تست عملی یک مدل نمونه ایجاد کن
from sqlalchemy import  Column, Integer, Float,String
from sqlalchemy.orm import declarative_base
from time import time
Base = declarative_base()
class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    product = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    time = Column(Integer, nullable=False)
    
    def __init__(self, order_id,product, price, time):
        self.order_id = order_id
        self.product = product
        self.price = price
        self.time = time
        


order_1={"order_id":1,"product":"produc_1","price":100,"time":time()}

order_2=Order(order_id=2, product="produc_2",price=200, time=time())


engine=SessionFactory("data.db").sqlite()
db=DatabaseManager(engine=engine,base=Base)
db.create_tables()
print(db.insert(Order(**order_1)))
print((db.insert(order_2)))

print(db.get(Order,limit=2).to_json())

>>> [
    {
        "order_id": 1,
        "price": 100.0,
        "product": "produc_1",
        "time": 1746916053.5904622
    },
    {
        "order_id": 2,
        "price": 200.0,
        "product": "produc_2",
        "time": 1746916053.5904622
    }
]
