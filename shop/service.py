from shop import conn


def get_categories():
    cursor = conn.cursor()
    cursor.execute("""select * from category""")
    records = cursor.fetchall()
    res = []
    for r in sorted(records, key=lambda x: len(x[0])):
        res.append({"id": r[0], "name": r[1]})
    return res


def get_products(cat_num):
    cursor = conn.cursor()
    cursor.execute("""select * from product where cat_num = %(cat_num)s order by price desc""", {"cat_num": cat_num})
    records = cursor.fetchall()
    res = []
    for r in records:
        res.append({"id": r[0], "name": r[1], "price": r[2], "installment_plan": r[3],
                    "warranty_period": r[4], "img_url": r[5], "description": r[6], "cat_num": r[7]})
    return res
