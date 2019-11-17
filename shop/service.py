from shop import conn


def get_categories():
    cursor = conn.cursor()
    cursor.execute("""select * from category""")
    records = cursor.fetchall()
    res = []
    for r in sorted(records, key=lambda x: len(x[0])):
        res.append({"id": r[0], "name": r[1]})
    return res
