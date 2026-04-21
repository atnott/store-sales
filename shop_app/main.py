from models import Shop

cart = [(1, 2)]
shop = Shop()
for p in shop.get_all_products():
    print(p)

for e in shop.get_all_employees():
    print(e)

success, result = shop.make_purchase(id_cashier=1, cart_items=cart)
print(result)

