from shop import conn


def get_categories():
    cursor = conn.cursor()
    cursor.execute("""select * from category""")
    records = cursor.fetchall()
    res = []
    for r in sorted(records, key=lambda x: len(x[0])):
        res.append({"id": r[0], "name": r[1]})
    return res


def get_node_categories():
    cursor = conn.cursor()
    cursor.execute("""select category.cat_num cat_num, category.cat_name from category where cat_num not in 
                  (select category.cat_num from product, category  where product.cat_num = category.cat_num)""")
    records = cursor.fetchall()
    res = []
    for r in sorted(records, key=lambda x: len(x[0])):
        res.append({"id": r[0], "name": r[1]})
    return res


def get_leaf_categories():
    cursor = conn.cursor()
    cursor.execute("""select cat_num, cat_name from category where cat_num not in (select distinct f.cat_num from 
                        category f, category f1 where f1.cat_num like f.cat_num || '.' || '%');""")
    records = cursor.fetchall()
    res = []
    for r in sorted(records, key=lambda x: len(x[0])):
        res.append({"id": r[0], "name": r[1]})
    return res


def add_category(data):
    cursor = conn.cursor()
    cursor.callproc('add_category', [len(data["parent"].split(".")) + 1, data["name"], data["parent"], ])
    conn.commit()


def update_category(data):
    cursor = conn.cursor()
    cursor.execute("""update category set cat_name = %(cat_name)s where cat_num = %(cat_num)s""",
                   {"cat_name": data["name"], "cat_num": data["id"]})
    conn.commit()


def remove_category(id):
    cursor = conn.cursor()
    cursor.execute("""delete from category where cat_num = %(cat_num)s;""", {"cat_num": id})
    cursor.execute("""delete from list_brand_product where prod_id IN 
                        (select prod_id from product where cat_num = %(cat_num)s);""", {"cat_num": id})
    cursor.execute("""delete from product where cat_num = %(cat_num)s;""", {"cat_num": id})
    conn.commit()


def get_products(cat_num):
    cursor = conn.cursor()
    cursor.execute("""select * from product where cat_num = %(cat_num)s order by price desc""", {"cat_num": cat_num})
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "description": r[6], "cat_num": r[7]})
    return res


def get_filtered_products(params):
    cursor = conn.cursor()
    cursor.execute("""select * from product where cat_num = %(category)s and 
        price >= %(minPrice)s and price <= %(maxPrice)s and warranty_period >= %(minWarranty)s and 
        warranty_period <= %(maxWarranty)s and installment_plan = %(installment)s order by price desc""", params)
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "description": r[6], "cat_num": r[7]})
    return res


def get_filter_values(cat_num):
    cursor = conn.cursor()
    cursor.execute("""select min(price), max(price), min(warranty_period), max(warranty_period) 
        from product where cat_num = %(cat_num)s""", {"cat_num": cat_num})
    records = cursor.fetchall()
    res = {"minPrice": 0, "maxPrice": 0, "minWarranty": 0, "maxWarranty": 0}
    if records:
        res = {"minPrice": records[0][0], "maxPrice": records[0][1], "minWarranty": records[0][2],
               "maxWarranty": records[0][3]}
    return res
