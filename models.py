class Promotion:
    def __init__(self, promotion_id, year, name, user_count):
        self.promotion_id = promotion_id
        self.year = year
        self.name = name
        self.user_count = user_count

    @classmethod
    def get_all_promotions(cls, mysql):
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT p.promotion_id, p.year, p.name, COUNT(u.user_id) as user_count
            FROM Promotions p
            LEFT JOIN Users u ON p.promotion_id = u.promotion_id
            GROUP BY p.promotion_id, p.year, p.name
            ORDER BY p.year DESC""")
        results = cur.fetchall()
        cur.close()

        promotions = []
        for row in results:
            promotion = cls(row[0], row[1], row[2], row[3])
            promotions.append(promotion)

        return promotions
