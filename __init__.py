from flask import Flask, render_template, request, redirect, url_for, send_file
from Forms import OrderForm
import shelve, User, Customer
import xlsxwriter
import base64
import json
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Order', methods=['GET','POST'])
def order():
    current_orders_dict = {}

    order_form = OrderForm(request.form)
    if request.method == 'POST' and order_form.validate():
        db = shelve.open('order.db', 'c')

        try:
            current_orders_dict = db['orders']
        except:
            print("Error in retrieving Customers from order.db.")

        customer = Customer.Customer(order_form.food.data, order_form.quantity.data,
                                     order_form.remarks.data, order_form.order_time.data)
        current_orders_dict[customer.get_customer_id()] = customer
        db['orders'] = current_orders_dict

        db.close()

        return redirect(url_for('home'))
    return render_template('Order.html', form=order_form)

@app.route('/CurrentOrders')
def current_orders():
    db = shelve.open('order.db', 'r')
    try:
        current_orders_dict = db['orders']
        print(current_orders_dict)
        db.close()
    except KeyError:
        print('Key Error')

    order_list = []
    for key in current_orders_dict:
        orders = current_orders_dict.get(key)
        order_list.append(orders)

    return render_template('CurrentOrders.html', count=len(order_list), order_list=order_list)

@app.route('/PastOrders')
def history_orders():
    db = shelve.open('history.db', 'c')
    try:
        history_orders_dict = db['orders']
        db.close()
    except KeyError:
        print('Key Error')

    history_list = []
    for key in history_orders_dict:
        orders = history_orders_dict.get(key)
        history_list.append(orders)

    return render_template('PastOrders.html', count=len(history_list), history_list=history_list)

@app.route('/complete_order/<int:id>', methods=['POST'])
def complete_order(id):
    if request.method == 'POST':
        source_db = shelve.open('order.db', 'c')
        destination_db = shelve.open('history.db', 'c')

        try:
            orders_dict = source_db.get('orders', {})
            if id in orders_dict:
                completed_order = orders_dict[id]
                # Copy the completed order to the history database
                history_dict = destination_db.get('orders', {})
                history_dict[id] = completed_order
                destination_db['orders'] = history_dict

                # Remove the completed order from the current orders
                orders_dict.pop(id, None)
                source_db['orders'] = orders_dict
            else:
                print(f"No order found with ID {id} in 'order.db'")
        except:
            print("Error")
        finally:
            source_db.close()
            destination_db.close()
        return redirect(url_for('home'))
    return render_template('CurrentOrders.html')

@app.route('/deleteOrder/<int:id>', methods=['POST'])
def delete_order(id):
    customers_dict = {}
    db = shelve.open('history.db', 'w')
    customers_dict = db['orders']
    customers_dict.pop(id)

    db['orders'] = customers_dict
    db.close()

    return render_template('PastOrders.html')

@app.route('/Dashboard')
def dashboard():
    print('hello world')

    db = shelve.open('history.db', 'r')
    try:
        pie_dict = db['orders']
    except:
        print('Error')

    food_list = ['Plain waffle', 'Chocolate Waffle', 'Peanut Butter Waffle']
    plain_list = []
    chocolate_list = []
    peanut = []
    print(pie_dict)
    for i in pie_dict:
        if i.get_food() == 'Plain Waffle':
            plain_list.append(i.get_quantity)
        elif i.get_food() == 'Chocolate Waffle':
            chocolate_list.append(i.get_quantity)

    db.close()

    return render_template('SalesDashboard.html', )

@app.route('/download_excel_api')
def downloadExcelApi():
    apiResponse = createApiResponse()
    return apiResponse

def createApiResponse():
    bufferFile = writeBufferExcelFile()
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    return send_file(bufferFile,mimetype=mimetype)
    return response

def writeBufferExcelFile():
    buffer = BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()

    dataHeader=["ID","Food", "Quantity","Remarks","Time"]
    headerStyle=workbook.add_format(createHeadStyle())
    worksheet.write_row(0,0,dataHeader,headerStyle)

    try:
        db = shelve.open('history.db', 'r')
        history_orders_dict = db['orders']
        db.close()
        history_list = []

        for key in history_orders_dict:
            var = history_orders_dict.get(key)
            history_list.append(var)
        print(history_list)
        
        '''for rowIndex, order in enumerate(history_list):
            OrderValues = list(order.values())'''
        format = workbook.add_format(createDataStyle())
        if len(history_list) % 2 == 1:
            format = workbook.add_format(createDataStyle('#e2efd9'))
        worksheet.write_row(len(history_list) + 1, 0, DataWritten(history_list), format)
        worksheet.set_column(1, 8, 27)

    except KeyError:
        print('Key Error')
    except OSError:
        print('OSError')
    
    workbook.close()
    buffer.seek(0)
    return buffer

def DataWritten(history_list):
    dataToBeWritten = []
    for orders in history_list:
        dataToBeWritten = [
            orders.get_customer_id(),
            orders.get_food(),
            orders.get_quantity(),
            orders.get_remark(),
            orders.get_order_time()
        ]
    
    return dataToBeWritten

def createDataStyle(bgColor='#FFFFFF'):
    dataStyle={
        'border': 1,
        'fg_color': bgColor
    }
    return dataStyle

def createHeadStyle():
    headStyle={
       'border': 1,
       'font_size':'12',
       'bold':True,
        'fg_color': '#00b050'
    }
    return headStyle

if __name__ == '__main__':
    app.run(debug=True)

