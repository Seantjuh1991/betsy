from peewee import *
from rich import print
import os

db = SqliteDatabase("database.db")

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name    = CharField()
    address = CharField()
    billing = CharField()

class Product(BaseModel):
    name        = CharField()
    description = CharField()
    price       = DoubleField()
    stock       = IntegerField()
    tag1        = CharField()
    tag2        = CharField()

class Catalog(BaseModel):
    name    = ForeignKeyField(User)
    product = CharField()

class Transaction(BaseModel):
    buyer    = ForeignKeyField(User)
    product  = ForeignKeyField(Product)
    quantity = IntegerField()     



def populate_test_database():

    db.connect()
    db.create_tables([User, Product, Catalog, Transaction])

    # Data        name             address                 billing
    userinfo = [["henk"   , "sesamstraat 4"       , "NL91BUNQ0909122334"],
                ["klaas"  , "korte langestraat 12", "NL24INGB0001234567"],
                ["sara"   , "Apendans 1"          , "NL11RABO1234122223"],
                ["suzanne", "Boerenverdriet 69"   , "NL38ABNA0001234556"],
                ["iris"   , "Vliegende koffer 24" ,"NL24INGB00071654321"]]

                # name          description      price    stock      tag1                 tag 2
    products = [["mouse"    , "logitech G500" ,   15.0,    10, "gaming mouse"      , "logitech"       ],
                ["keyboard" , "logitech G910" ,   60.0,    25, "gaming keyboard"   , "logitech"       ],
                ["monitor"  , "samsung 49inch",  199.0,    10, "gaming monitor"    , "samsung 49 inch"],
                ["monitor"  , "samsung 24inch",  159.0,     5, "monitor"           , "samsung 23 inch"],
                ["headset"  , "sony WH400"    ,  399.0,     3, "headset accesoires", "sony WH400"     ],
                ["chair"    , "dx racer"      ,  259.0,    10, "seat racing"       , "dx"             ],
                ["laptop"   , "apple macbook" , 1999.0,     5, "macbook air"       , "apple"          ]]

    # Inject data
    for u in userinfo:
        User.create(name=u[0], address=u[1], billing=u[2])
    
    for p in products:
        Product.create(name=p[0], description=p[1], price=p[2], stock=p[3], tag1=p[4], tag2=p[5])

    db.close()
    print("[green]Database has been successfully filled![/green]")


def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "database.db")
    if os.path.exists(database_path):
        os.remove(database_path)
        print("[green]Database successfully removed![/green]")
    else:
        print("[red]Database not found.[/red]")