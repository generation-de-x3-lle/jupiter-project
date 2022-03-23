import csv
from datetime import datetime
def extract_csv():
    products_price_list=[]
    
    try:
    
        with open('Chesterfield.csv', 'r', newline='') as file:
            extracted_list=[]
            header=['Date', 'Location', 'name', 'product', 'total','payment_method', 'card_number']
            reader=csv.DictReader(file,header)

            for row in reader:
        
                #Split date/time
                transaction_date_time = row['Date'].split(' ')
                date = {'Date': transaction_date_time[0]}
                time= {'Time': transaction_date_time[1]}
            
                new_date=datetime.strptime(transaction_date_time[0],'%d/%m/%Y').strftime('%m/%d/%Y')
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

    except Exception as extype:
        exception_template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        exception_message = exception_template.format(type(extype).__name__, extype.args)
    return exception_message
    