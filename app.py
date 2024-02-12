from flask import Flask, render_template, url_for, request, redirect, flash, session
from Forms import RegistrationForm, LoginForm, EditUserForm, ChangePasswordForm, ForgotPasswordForm
from customer_login import CustomerLogin, RegisterCustomer, EditDetails, ChangePassword, securityQuestions
from customer import Customer
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_bcrypt import Bcrypt
from io import BytesIO
from store_owner import StoreOwner
from store_owner_login import StoreOwnerLogin, CreateStoreOwner, storeOwners
import shelve, sys, Customer, xlsxwriter, base64, json


app = Flask(__name__)
bcrypt = Bcrypt(app)


app.config['SECRET_KEY'] = 'The_secret_key'
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):        
    with shelve.open('userdb', 'c') as userdb:
        for keys in userdb:
            if keys == id:
                return userdb[id]

login_manager.init_app(app)

#home page
@app.route('/')
def home():
    return render_template('home.html')

#order page
@app.route('/order')
@app.route('/order/<store_name>')
def order():
    return render_template('order.html')


#About us pages
@app.route('/openingHours')
def openingHours():
    return render_template('openingHours.html')

@app.route('/findUs')
def findUs():
    return render_template('findUs.html')

@app.route('/contactUs')
def contactUs():
    return render_template('contactUs.html')

#Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            user = CustomerLogin(form.phoneNumber.data, form.password.data)
            if isinstance(user, Customer):
                for keys in userdb:
                    if user.get_id() == keys:
                        if bcrypt.check_password_hash(userdb[keys].get_password(), form.password.data):
                            if form.remember.data == True:
                                login_user(userdb[keys], remember=True)
                            else:
                                login_user(userdb[keys])
                            session['id'] = user.get_id()
                            return render_template('home.html', logined = True)

            else:
                flash("wrong username/password. please try again")
                return redirect(url_for('login'))
    return render_template('login.html', form=form)


#Store Owner Login
@app.route('/storeOwnerLogin', methods=["POST", "GET"])
def storeOwnerLogin():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('SOdb', 'c') as SOdb:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = StoreOwnerLogin(form.phoneNumber.data, hashed_password)
            if isinstance(user, StoreOwner):
                print(isinstance(user, StoreOwner))
                print(len(SOdb))
                for keys in SOdb:
                    print(keys)
                    print(user.get_phoneNumber())
                    if user.get_phoneNumber() == SOdb[keys].get_phoneNumber():
                        if bcrypt.check_password_hash(SOdb[keys].get_password(), user.get_password()):
                            if form.remember.data == True:
                                login_user(SOdb[keys], remember=True)
                            else:
                                login_user(SOdb[keys])
                            session['id'] = user.get_id()
                            return render_template('home.html')

            else:
                flash("wrong username/password. please try again")
                return redirect(url_for('storeOwnerLogin'))
    return render_template('storeOwnerLogin.html', form=form)







@app.route('/forgotPassword', methods=["Get", "POST"])
def forgotPassword():
        
    secQn = None
    form = ForgotPasswordForm(request.form)
    if request.method == "POST":
        user = Customer(form.phoneNumber.data)
        with shelve.open('userdb', 'c') as userdb:
            for key in userdb:
                if key == user.get_id():
                    
                    secQn = securityQuestions[int(userdb[key].get_securityQuestion())]
                    if form.validate():
                        if userdb[key].get_securityAnswer() == form.securityAnswer.data.strip().title():
                            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
                            user = userdb[key]
                            user.set_password(hashed_password)
                            if isinstance(user, Customer):
                                userdb[key] = user
                                flash("Password successfully reset.", "success")
                                return redirect(url_for("login"))
                            
                            else:
                                flash("something went wrong", "warning")
                                return redirect(url_for('forgotPassword'))

                    elif form.securityAnswer.data == None:
                        return render_template("forgotPassword.html", form=form, secQn = secQn)
                    
                    else:
                        flash("Incorrect Security Question Answer", "warning")
                        return redirect(url_for('forgotPassword'))
    return render_template("forgotPassword.html", form=form, secQn = secQn)

#Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            if str(form.phoneNumber.data) not in userdb:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                formattedSecurityQuestionAnswer = form.securityAnswer.data.strip().title()
                user = RegisterCustomer(form.name.data, form.phoneNumber.data, hashed_password, form.gender.data, form.securityQuestion.data, formattedSecurityQuestionAnswer)
                if isinstance(user, Customer):
                    userdb[user.get_id()] = user
                    flash('Registration Successful!', "success")
                    return redirect(url_for('login'))
            else:
                flash("Already registered please login instead" , 'success')
                return redirect(url_for('login'))
    return render_template('register.html', form=form)

#profile page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    shownGender = str(current_user.get_gender())
    form = EditUserForm(request.form, gender = shownGender)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            user = EditDetails(form.phoneNumber.data, form.name.data, form.gender.data)
            if isinstance(user, Customer):
                for key in userdb:
                    if user.get_id() == key:
                        user = userdb[key]
                        user.set_name(form.name.data)
                        user.set_id(form.phoneNumber.data)
                        user.set_gender(form.gender.data)
                        userdb[key] = user
            flash('Successfully edited', 'success')
            return redirect(url_for('profile'))
        
    return render_template('profile.html', form=form)

#change password page
@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            new_hashed_password = bcrypt.generate_password_hash(form.newPassword.data).decode('utf-8')
            if bcrypt.check_password_hash(current_user.get_password(), form.password.data):
                user = ChangePassword(current_user.get_id(), new_hashed_password)
                print(user.get_id())
                for keys in userdb:
                    if keys == user.get_id():
                        user = userdb[keys]
                        user.set_password(new_hashed_password)
                        if isinstance(user, Customer):
                            userdb[keys] = user
                            flash("Password changed successfully", "success")
                            return redirect(url_for('home'))
            else:
                flash("Password change unsuccessful", "danger")
                return redirect(url_for('changePassword'))

    return render_template('changePassword.html', form=form)


@app.route('/deleteProfile', methods = ["POST", "GET"])
@login_required
def deleteProfile():
    form = request.form
    if request.method == "POST":
        if request.form.get('Delete') == 'Delete':
            with shelve.open('userdb', 'c') as userdb:
                for key in userdb:
                    if current_user.get_id() == key:
                        print("Slay")
                        del userdb[key]
                        userdb.sync()
                        flash("Profile deleted. Please register for future use.", "success")
                        session.pop('id')
                        logout_user
                        return redirect(url_for('home'))
        elif  request.form.get('Cancel') == 'Cancel':
            flash("Profile deletion aborted", "warning")
            return redirect(url_for('profile'))
        else:
            pass
    elif request.method == 'GET':
        return render_template('deleteProfile.html', form=form)

    return render_template('deleteProfile.html')

@app.route('/dbCheck')
def dbCheck():
    user_list = []
    with shelve.open('userdb', 'c') as userdb:
        if len(userdb) == 0:
            raise 404

        else:
            for key in userdb:
                user_list.append(userdb[key])

    return render_template("dbCheck.html", user_list=user_list)


#Logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('id')
    flash("User successfully logged out." , 'success')
    return redirect(url_for("home"))


#Error handling
@app.errorhandler(401)
def not_authorised(error):
        return render_template('error.html', error_code = 401, message = "Please login to view this page")
    
@app.errorhandler(404)
def not_found(error):
        return render_template('error.html', error_code = 404, message = 'Page not found. Sorry for the inconvinience caused.')
    
@app.errorhandler(500)
def unknown_error(error):
        return render_template('error.html', error_code = 500, message='Unknown error occured')
    
# @app.errorhandler(AttributeError)
# def attribute_error(error):
#         return render_template('error.html', error_code = AttributeError)


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
    peanut_list = []
    print(pie_dict)
    for order in pie_dict:
        print(i)
        if 'Plain Waffle' in order:
            plain_list.append(order.get_quantity())
        elif order.get_food() == 'Chocolate Waffle':
            chocolate_list.append(order.get_quantity())
        elif order.get_food() == "Peanut Butter Waffle":
            peanut_list.append(order.get_quantity())

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
    app.run(debug = True)