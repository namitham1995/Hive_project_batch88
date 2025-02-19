from pyhive import hive
import hive_fns
import analytics
import numpy as np
try:
    c=hive.connect(host="localhost",database="batch88").cursor()
    print('Connection established........')
    data_path="/home/oem/Downloads/online_sales_dataset.csv"
    try:
       c.execute(hive_fns.create_table('online_sales',hive_fns.online_sales_columns,','))
       c.execute(hive_fns.insert_data(data_path,'online_sales'))
       print("Table created successfully")
    except Exception as e:
       print('Error in table creation')
    # Analytics
    # 1.which payment method has more transaction
    try:
        c.execute(analytics.analytics_1())
        print(f'Number of transactions in each payment method :{c.fetchall()}')
    except Exception as e:
        print(f'Error in analytics one: {e}')
    # 2 . No.of orders in each Warehouse with visualization
    c.execute(analytics.analytics_2())
    # print(c.fetchall())
    result=c.fetchall()
    print(f'Number of orders in Warehouse :{result}')
    x_values=[]
    y_values=[]
    for i in result:
        if i[0]!='' and i[0]!=None:
            x_values.append(i[0])
            y_values.append(i[1])
    # analytics.plot_bar_graph(x_values, y_values, 'orders in warehouse', 'warehouse', 'count')
    # 3 .find average shipping cost in each country
    c.execute(analytics.analytics_3())
    print(f'Average shipping cost in each country : {c.fetchall()}')
    # 4 .find number of different mode of transaction in each country
    print('Result of Analytics Four ..........')
    c.execute(analytics.analytics_4())
    c.execute('select distinct country from c_transaction')
    x_names = c.fetchall()
    c.execute('select * from c_transaction')
    x_values = np.arange(1,len(x_names)+1)
    y_values = c.fetchall()
    bt = []
    cc = []
    pp = []
    for i in y_values:
        if i[1] == 'Bank Transfer':
            bt.append(i[2])
        elif i[1] == 'Credit Card':
            cc.append(i[2])
        elif i[1] == 'paypall':
            pp.append(i[2])

    analytics.graph_2(x_values,x_names,bt,cc,pp)
except Exception as e:
    print(f'Error in connection: {e}')





























