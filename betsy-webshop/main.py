__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
import models
from rich import print


# POPULATE DATABASE
#models.populate_test_database()


# DELETE DATABASE
#models.delete_database()



# Upgraded the search functionality by adding another argument. Table is used to specify which table to search in.
def search(term, table=None):
    match table:

        # Standard product search function
        case None:
            product_exists = False
            for p in Product:
                if term in p.name:
                    print(f"[blue]Name: {p.name}, Description: {p.description}, Price: {p.price}, Stock: {p.stock}, Tag1: {p.tag1}, Tag2: {p.tag2}[/blue]")
                    product_exists = True
            if product_exists == False:
                print(f"[red]Product '{term}' not found![/red]")

        # Search if user exists
        case "user":
            for u in User:
                if str(term) == u.name or str(term) == str(u.id):
                    return True
            print(f"[red]User '{term}' not found![/red]")

        # Search if product exists
        case "product":            
            for p in Product:
                if str(term) == str(p.name) or str(term) == str(p.id):
                    return True
            print(f"[red]Product '{term}' not found![/red]")

        # Search on tags
        case "tag":
            tag_found = False
            for p in Product:
                if term in p.tag1 or term in p.tag2:
                    print(f"[blue]Name: {p.name}, Description: {p.description}, Price: {p.price}, Stock: {p.stock}, Tag1: {p.tag1}, Tag2: {p.tag2}[/blue]")
                    tag_found = True
            if tag_found == False:
                print(f"[red]No product matching with tag: '{term}'.[/red]")

        # Search catalog
        case "catalog":
            for c in Catalog:
                if term in str(c.product):
                    return True
            return False        

# TEST
#search("keyboard")

# Stored in catalog table
def list_user_products(user_id):  
    # Check if user exists
    if search(user_id,"user"):
        users = User.get(User.id==user_id)
        print(f"[green]The following items from user {users.name} have been found:[/green]")
        for c in Catalog.select().where(Catalog.name==user_id):
            print(f"[blue]{c.product}[/blue]")

# TEST  
#list_user_products(5)

# Search on tag, don't have to specify full words
def list_products_per_tag(tag): 
    search(tag,"tag")

#TEST
#list_products_per_tag("gaming")    

# Uses a table to link sellers to products, User can have 1 of the same product.
def add_product_to_catalog(user_id, product):  

    # Check if user and product exists
    if search(user_id,"user") and search(product,"product"):
        users = User.get(User.id==user_id)

        # Check if product not already in catalog by user
        for user in Catalog.select().where(Catalog.name==user_id):
            if product == user.product:
                print(f"[red]{product} is already in {users.name}'s catalog[/red]")
                return

        # Add to catalog
        Catalog.create(name=user_id, product=product)    
        print(f"[green]{product} added to {users.name}'s catalog[/green]")    
       
# TEST
#add_product_to_catalog(5,"keyboard") 

# Simply updates the stock 
def update_stock(product_id, new_quantity):
    # Check if product exists
    if search(str(product_id),"product"):
        stock = Product.get(Product.id==product_id)
        print(f"[green]Stock from {stock.name} is updated from {stock.stock} -> {new_quantity}[/green]")
        stock.stock = new_quantity
        stock.save()

# TEST
#update_stock(1,20)    

# Writes a purchase history in a table, buyer can only be a user
def purchase_product(product_id, buyer_id, quantity):
    # Check if product and buyer (user) exists.
    if search(product_id,"product") and search(buyer_id,"user"):
        users = User.get(User.id==buyer_id)

        # Check if there is enough stock
        stock = Product.get(Product.id==product_id)
        if quantity <= stock.stock:
            print(f"[green]{users.name} bought {quantity} {stock.name}(s)[/green]")
            new_quantity = stock.stock - quantity
            update_stock(product_id,new_quantity)
            Transaction.create(buyer=buyer_id, product=product_id, quantity=quantity)
        else:
            print(f"[red]Not enough {stock.name}(s) in stock![/red]")
        
# TEST
#purchase_product(3,1,2)


# Remove product from Product table
def remove_product(product_id):
    # First check if product exists
    if search(str(product_id),"product"):
        instance = Product.get(Product.id==product_id)
        print(f"[green]Product: {instance.name} has been successfully removed![/green]")
        instance.delete_instance()

#TEST
#remove_product(1)      