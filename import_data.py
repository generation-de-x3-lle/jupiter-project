import psycopg2
from extract_csv import extract_csv
#Establish the connection, use this when creating the databse first time
conn = psycopg2.connect(
    host="localhost",
    database="cafes_db",
    user="root",
    password="password")
conn.autocommit = True
cur = conn.cursor()

cafe_chesterfield_data = extract_csv()

for data_row in  cafe_chesterfield_data:
    data_row_insert_sql = f"""INSERT INTO transactions(transaction_date,transaction_time,payment_method,total_purchase,location)
            VALUES('{data_row['Date']}','{data_row['Time']}','{data_row['payment_method']}','{data_row['total']}','{data_row['Location']}') RETURNING transaction_id"""    
    cur.execute(data_row_insert_sql)

    transaction_id = cur.fetchone()[0]

    for each_product_dict in data_row['products']:
        product_row_insert_sql = f"""INSERT INTO basket(item_name,item_price) VALUES(
        '{each_product_dict['product']}','{each_product_dict['price']}') RETURNING basket_item_id"""

        cur.execute(product_row_insert_sql)
        
        basket_row_id=cur.fetchone()[0]

        basket_transaction_insert_sql = f"""INSERT INTO transaction_basket(transaction_id,basket_item_id)
        VALUES('{transaction_id}','{basket_row_id}')"""
        cur.execute(basket_transaction_insert_sql)

cur.close
conn.close