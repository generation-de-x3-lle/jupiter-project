import json
import psycopg2 
import boto3 # library used to access AWS API
import os
import codecs
import csv
import datetime



def load_s3():

    listofdicts=[]
    products_price_list=[]
    extracted_list=[]
    fieldnames =['Date','Location','name','product','total','payment_method','card_number']
    os.chdir('/tmp')
    bucket = 'de-x3-lle-jupiter'
    filename = '2022/3/16/chesterfield_16-03-2022_09-00-00.csv'
    client = boto3.client('s3')
    response = client.get_object(
    Bucket=bucket,
    Key=filename
    )#['Body'].read().decode('utf-8') 
    
    for rows in csv.DictReader(codecs.getreader("utf-8")(response["Body"]),fieldnames=fieldnames):
    
        listofdicts.append(rows)
        
    return listofdicts

def transform_data(listofdicts):
    
    products_price_list=[]
    extracted_list=[]

    for row in listofdicts:
    
            #Split date/time
            transaction_date_time = row['Date'].split(' ')
            date = {'Date': transaction_date_time[0]}
            time= {'Time': transaction_date_time[1]}
        
            new_date=datetime.datetime.strptime(transaction_date_time[0],'%d/%m/%Y').strftime('%m/%d/%Y')
            date = {'Date': new_date}
    
            row.update(date)
            row.update(time)
            
            if row['payment_method']=='CASH':
                row.pop('card_number')
            if '' not in row.values():
    
                products_split=row['product'].split(',')
    
                for each_product in products_split:
    
                    product_price=each_product[-4:]
                    product=each_product[:len(each_product)-7]
                    product = product.strip()
                    product_price=product_price.strip()
                    
                    single_product_dict={'product': product,'price': product_price}
                    products_price_list.append(single_product_dict)
                    single_product_dict={}
    
                row.pop('name')
                if 'card_number' in row:
    
                    row.pop('card_number')
    
                row['products']=products_price_list
                extracted_list.append(row)
                products_price_list=[]
        
    return extracted_list
            
            
def load_data(extracted_list):
    print('Making a connection')
    conn=psycopg2.connect(dbname = '*****',
                          host = '******',
                          port = '****',
                          user = '****',
                          password ='********')
    print('connection successfull')
    print(conn.info)
    cur=conn.cursor()
    
    
    for data_row in  extracted_list:
        data_row_insert_sql = f"""INSERT INTO jupiter.transactions(transaction_date,transaction_time,payment_method,total_purchase,location)
                VALUES('{data_row['Date']}','{data_row['Time']}','{data_row['payment_method']}','{data_row['total']}','{data_row['Location']}') """    
        cur.execute(data_row_insert_sql)
        conn.commit()

        Query = "Select top 1 transaction_id from jupiter.transactions Order by transaction_id Desc;"
        cur.execute(Query)
        
        transaction_id=cur.fetchone()[0]
        conn.commit()
        
        for each_product_dict in data_row['products']:
            product_row_insert_sql = f"""INSERT INTO jupiter.basket(item_name,item_price) VALUES(
            '{each_product_dict['product']}','{each_product_dict['price']}') """

            cur.execute(product_row_insert_sql)
            conn.commit()
        
            Query = "Select top 1 basket_item_id from jupiter.basket Order by basket_item_id Desc;"
    
            cur.execute(Query)
            basket_row_id=cur.fetchone()[0]
            conn.commit()
  
            basket_transaction_insert_sql = f"""INSERT INTO jupiter.transaction_basket(transaction_id,basket_item_id)
            VALUES('{transaction_id}','{basket_row_id}')"""
            cur.execute(basket_transaction_insert_sql)
            conn.commit()


def lambda_handler(event, context):
    
    loaded_extract_list=load_s3()

    staging_list=transform_data(loaded_extract_list)
    
    load_data(staging_list)



