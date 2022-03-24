#Make the required imports
import psycopg2

#Make a connection to Redshift
conn=psycopg2.connect(
    dbname = 'jupiter',
    host = '########',
    port = '###',
    user = '####',
    password = '#####')

print('connection successfull')
print(conn.info)
cur=conn.cursor()

#Make a schema called jupiter in Redshift
Query= 'create schema if not exists jupiter;'
cur.execute(Query)
conn.commit()

#Create Basket table
create_basket_table = """
CREATE TABLE jupiter.basket (
    basket_item_id int IDENTITY(1,1),
    item_name VARCHAR (200),
    item_price numeric (9,2),
    primary key(basket_item_id)
    );
""" 
cur.execute(create_basket_table)
conn.commit()

#Create Transaction table, date(year,month,day) 
create_transaction_table = """
CREATE TABLE jupiter.transactions (
    transaction_id  int IDENTITY(1,1),
    transaction_date date not null,
    transaction_time time not null,
    payment_method VARCHAR (100),
    total_purchase numeric (19,2),
    location VARCHAR (100),
    primary key (transaction_id)
);
"""
cur.execute(create_transaction_table)
conn.commit()

#Create table Transation_basket table

create_transaction_basket_table = """
CREATE TABLE jupiter.transaction_basket (
    basket_id int IDENTITY (1,1),
    transaction_id int,
    basket_item_id int,
    primary key (basket_id),
    foreign key (transaction_id) references jupiter.transactions(transaction_id),
    foreign key (basket_item_id) references jupiter.basket (basket_item_id)
    );
""" 
cur.execute(create_transaction_basket_table)
conn.commit()
cur.close()
conn.close()