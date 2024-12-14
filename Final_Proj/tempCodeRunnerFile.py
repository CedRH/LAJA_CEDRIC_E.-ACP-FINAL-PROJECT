cursor.execute(formatted_query, tuple(product_ids))
        cart_products = cursor.fetchall()