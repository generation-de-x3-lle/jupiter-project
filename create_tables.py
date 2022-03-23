#Make all the required imports
import psycopg2
#Establish the connection, use this when creating the databse first time
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="root",
    password="password")
conn.autocommit = True
cur = conn.cursor()

#Create database, use this when creating the database first time
create_database = '''CREATE DATABASE cafes_db;'''
cur.execute(create_database)
cur.close()
conn.close()

# New connection to the database cafe_db, as new database has been created need to change the conn database
conn = psycopg2.connect(
    host="localhost",
    database="cafes_db",
    user="root",
    password="password")
conn.autocommit = True
cur = conn.cursor()



#Create Basket table
create_basket_table = """
CREATE TABLE basket (
    basket_item_id SERIAL PRIMARY KEY,
    item_name VARCHAR (200),
    item_price decimal (9,2)
    );
""" 
cur.execute(create_basket_table)

#Create Transaction table 
create_transaction_table = """
CREATE TABLE transactions (
    transaction_id  SERIAL PRIMARY KEY,
    transaction_date date not null,
    transaction_time time not null,
    payment_method VARCHAR (100),
    total_purchase decimal(19,2),
    location VARCHAR (100)
);
"""
cur.execute(create_transaction_table)


#Create table Transation_basket table

create_transaction_basket_table = """
CREATE TABLE transaction_basket (
    basket_id SERIAL PRIMARY KEY,
    transaction_id int,
    basket_item_id int,
    foreign key (transaction_id) references transactions(transaction_id),
    foreign key (basket_item_id) references basket (basket_item_id)
    );
""" 
cur.execute(create_transaction_basket_table)


cur.close()
conn.close()