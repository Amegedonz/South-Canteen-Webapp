from flask import Flask, render_template, url_for, request, redirect, flash, session
from Forms import RegistrationForm, LoginForm, DeleteUserForm, CustOrderForm
from customer_login import CustomerLogin, RegisterCustomer, DeleteCustomer
from customer import Customer
from customer_order import CustomerOrder, newOrderID
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
import shelve
import stripe
import uuid

app = Flask(__name__)

stripe.api_key = "sk_test_51OboMaDA20MkhXhqx0KQdxFgKbMYsLGIciIpWAKrwhXhXHytVQkPncx6SPDL79SOW0fdliJpbUkQ01kq5ZDdjYmP00nojJWp0p"

menu = {
    "Vegetarian": {
        "Bee Hoon": 2,
        "Spring rolls": 3,
        "Fried rice": 2.5
    },
    "Muslim": {
        "Rice" : 1,
        "Curry Chicken": 0.7,
        "Fried egg": 0.5,
        "Chicken wing": 0.7
    },
    "Indian": {
        "Dosa": 2.5,
        "Plain prata": 1.5,
        "Egg prata": 2
    },
    "Chicken Rice": {
        "Roasted chicken rice": 3,
        "Steamed chicken rice": 3,
        "Char siew rice": 3.5,
        "Roasted pork rice": 3.5,
        "Curry chicken rice": 3.5
    },
    "Pizza": {
        "Cheese pizza": 4,
        "Mac and cheese": 3.8
    },
    "Japanese": {
        "Salmon don": 3.8,
        "Kaarage": 2.5
    },
    "Ban Mian": {
        "Ban mian": 3,
        "Dumplings": 2.5,
        "Tom yum U mian": 3,
        "Mala U mian": 3,
        "Fish slice soup with bee hoon": 3.2
    },
    "Curry Rice": {
        "Chicken cutlet curry rice": 3.5,
        "Curry rice": 3,
        "Pork cutlet curry rice": 3.5,
        "Fried ebi curry rice": 3.5
    },
    "Yong Tau Foo": {
        "Wongbok": 0.5,
        "Tau pok": 0.5,
        "Tau kwa": 0.5,
        "Fishball": 0.5,
        "Fishcake": 0.5,
        "Enoki mushroom": 0.5,
        "Luncheon meat": 0.7,
        "Koka noodles": 0.5
    },
    "Mala": {
        "Vegetable": 0.7,
        "Meat": 0.9
    },
    "Bubble Tea": {
        "Milk tea": {"Base": 2, "White pearl": 0.5, "Black pearl": 0.5, "Nata de coco": 0.5},
        "Green milk tea": {"Base": 2, "White pearl": 0.5, "Black pearl": 0.5, "Nata de coco": 0.5},
        "Jasmine green tea": {"Base": 2, "White pearl": 0.5, "Black pearl": 0.5, "Nata de coco": 0.5},
        "Oolong milk tea": {"Base": 2, "White pearl": 0.5, "Black pearl": 0.5, "Nata de coco": 0.5},
        "Brown sugar milk tea": {"Base": 2, "White pearl": 0.5, "Black pearl": 0.5, "Nata de coco": 0.5},
        "Honey milk tea": {"Base": 2, "White pearl": 0.5, "Black pearl": 0.5, "Nata de coco": 0.5},
        "Strawberry milk tea": {"Base": 2, "White pearl": 0.5, "Black pearl": 0.5, "Nata de coco": 0.5},
    },
    "Takoyaki": {
        "Ham and cheese takoyaki": 4,
        "Octopus takoyaki": 4.5
    },
    "Snack": {
        "Muah Chee": 2.5,
        "Sandwich": 2
    },
    "Waffle": {
        "Chocolate waffle": 2.5,
        "Plain waffle": 2
    },
    "Drinks": {
        "Kopi": 1,
        "Teh": 1
    }
}

app.config['SECRET_KEY'] = 'your_secret_key'
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
                        if form.remember.data == True:
                            login_user(user, remember=True)
                            session['id'] = user.get_id()
                            return redirect('/')
                        login_user(user)
                        session['id'] = user.get_id()
                        return redirect('/')

            else:
                flash("wrong username/password. please try again")
                return redirect(url_for('login'))
    return render_template('login.html', form=form)

#Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            if str(form.phoneNumber.data) not in userdb:
                user = RegisterCustomer(form.name.data, form.phoneNumber.data, form.password.data, form.gender.data, form.securityQuestion.data, form.securityAnswer.data)
                if isinstance(user, Customer):
                    userdb[user.get_id()] = user
                    flash('Registration Successful!', "success")
                    return redirect(url_for('login'))
            else:
                flash("Already registered please login instead" , 'success')
                return redirect(url_for('login'))
    return render_template('register.html', form=form)

#edit page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            user = RegisterCustomer(form.name.data, form.phoneNumber.data, form.password.data, form.gender.data, form.securityQuestion.data, form.securityAnswer.data)
            if isinstance(user, Customer):
                userdb[str(user.get_id())] = user
                flash('Successfully edited')
            else:
                flash('Edit not successful')

    return render_template('edit.html', form=form)


#delete users page
@app.route('/deleteUser', methods=['GET', 'POST'])
def deleteUsers():
    form = DeleteUserForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open('userdb', 'c') as userdb:
            user = DeleteCustomer(form.phoneNumber.data, form.password.data)
            if isinstance(user, Customer):
                count = 0
                for keys in userdb:
                    count += 1
                    if keys == user.get_id():
                        del(userdb[user.get_id()])
                        flash('Successfully deleted')

                    if count == len(userdb):
                        flash('delete not successful')
            

    return render_template('deleteUser.html', form=form)


@app.route('/dbCheck')
@login_required
def dbCheck():
    user_list = []
    with shelve.open('userdb', 'c') as userdb:
        if len(userdb) == 0:
            raise 404

        else:
            for key in userdb:
                if key == session['id']:
                    print(userdb[key])

    return render_template("dbCheck.html", user_list=user_list)


@app.route('/custOrder')
def custOrder():
    return render_template('custOrder.html', menu=menu)

@app.route('/Vegetarian', methods=['GET', 'POST'])
@app.route('/Muslim', methods=['GET', 'POST'])
@app.route('/Indian', methods=['GET', 'POST'])
@app.route('/Chicken Rice', methods=['GET', 'POST'])
@app.route('/Pizza', methods=['GET', 'POST'])
@app.route('/Japanese', methods=['GET', 'POST'])
@app.route('/Ban Mian', methods=['GET', 'POST'])
@app.route('/Curry Rice', methods=['GET', 'POST'])
@app.route('/Yong Tau Foo', methods=['GET', 'POST'])
@app.route('/Mala', methods=['GET', 'POST'])
@app.route('/Bubble Tea', methods=['GET', 'POST'])
@app.route('/Takoyaki', methods=['GET', 'POST'])
@app.route('/Snack', methods=['GET', 'POST'])
@app.route('/Waffle', methods=['GET', 'POST'])
@app.route('/Drinks', methods=['GET', 'POST'])
@login_required
def stalls():
    path = request.path
    stall_name = path.lstrip('/')
    form = CustOrderForm(request.form)
    if request.method == 'POST' and form.validate():
        form.stall.data = stall_name
        form.orderID.data = str(newOrderID())
        form.phoneNumber.data = current_user.get_id()
        form.item.data = request.form.get('item')
        form.itemQuantity.data = request.form.get('itemQuantity')
        #form.ingredient.data = request.form.get('ingredient')
        #form.ingredientQuantity.data = request.form.get('ingredientQuantity')
        form.price.data = request.form.get('price')
        form.total.data = request.form.get('total')
        order = CustomerOrder(form.phoneNumber.data)
        order.set_id(current_user.get_id())
        order.set_stall(form.stall.data)
        order.set_orderID(form.orderID.data)
        order.set_item(form.item.data)
        order.set_itemQuantity(form.itemQuantity.data)
        #order.set_ingredient(form.ingredient.data)
        #order.set_ingredientQuantity(form.ingredientQuantity.data)
        order.set_price(form.price.data)
        order.set_total(form.total.data)
        order.set_remarks(form.remarks.data)
        order.set_status(form.status.data)
        with shelve.open('orderdb', 'c') as orderdb:
            orderdb[order.get_orderID] = order
            return redirect(url_for('stalls', stall_name=stall_name))


    return render_template(f'{stall_name}.html', menu=menu, stall_name=stall_name, form=form)


#Cart
@app.route('/cart')
@login_required
def cart():
    with shelve.open('orderdb', 'c') as orderdb:
        orders = []
        total = 0.0
        for order in orderdb:
            if orderdb[order].get_id() == current_user.get_id():
                orders.append(orderdb[order])
                total += float(orderdb[order].get_price)
        print(orders)
    return render_template('cart.html', menu=menu, orders=orders, total=total)

def calculate_amount():
    with shelve.open('orderdb', 'c') as orderdb:
        orders = []
        total = 0.0
        for order in orderdb:
            if orderdb[order].get_id() == current_user.get_id():
                orders.append(orderdb[order])
                total += float(orderdb[order].get_price)
    return total

price_id = "price_1ObuyUDA20MkhXhqmqe3Niwb"


@app.route("/checkout")
@login_required
def payment():
    try:
        amount = calculate_amount()

        
        stripe.Price.modify(
        "price_1ObuyUDA20MkhXhqmqe3Niwb",
        active=True, #change to false
        )

        stripe.Price.create(
        product='prod_PQmX9ciU3SUHVk',
        unit_amount_decimal=amount*100,
        currency="sgd",
        lookup_key="pricing",
        active=True
        )

        stripe.Product.modify(
        "prod_PQmX9ciU3SUHVk",
        default_price="price_1Oj2A3DA20MkhXhq3AHH5RXA",
        
        )

    except stripe.error.StripeError as e:
        print(f"Error updating price: {e}")
    return redirect("https://buy.stripe.com/test_aEU2889cUbLX1LacMR")

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
    


if __name__ == '__main__':
    app.run(debug = True)