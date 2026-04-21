from models import Shop

shop = Shop()
for p in shop.get_all_products():
    print(p)

for e in shop.get_all_employees():
    print(e)

