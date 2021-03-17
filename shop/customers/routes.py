from flask import render_template, session, redirect, request, url_for, flash, current_app, make_response
from shop import app, db, photos, bcrypt, login_manager
from .forms import CustomerRegistrationForm, CustomerLoginForm
from .models import Customer, Order
from flask_login import login_user, current_user,login_required, logout_user
import secrets, os
import pdfkit
from shop.products.models import Addproduct





@app.route('/customer/register', methods=['GET','POST'])
def customer_registration():
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Customer(name = form.name.data, username = form.username.data, email = form.email.data, password= hashed_password,country = form.country.data,\
            state = form.state.data,city = form.city.data,address = form.address.data,pin = form.pincode.data,contact = form.contact.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Thank you for regestering!  You are now able to log in!', 'success')
        return redirect(url_for('customer_login')) 
    return render_template('customer/register.html',title = 'Register', form = form)  


@app.route('/customer/login', methods=['GET','POST']) 
def customer_login():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            
            return redirect(url_for('home'))
        elif user is None:
            flash(f'You are not a registered customer. Registered yourself first!', 'danger')    
        else:    
            flash(f'Login Unsuccessful. Please check email or password','danger')
            return redirect(url_for('customer_login'))
    return render_template('customer/login.html',title = 'Login', form = form)            


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))    



@app.route('/getorder') 
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = Order(invoice = invoice, orders =session['shoppingcart'], customer_id = customer_id)
            db.session.add(order)
            db.session.commit()
            session.pop('shoppingcart')
            flash(f'Your order has been accepted', 'success')
            return redirect(url_for('order_detail', invoice = invoice))
        except Exception as e:
            print(e)
            flash(f'Something went wrong','danger')
            return redirect(url_for('allcart'))


@app.route('/orders/<invoice>')
@login_required
def order_detail(invoice):
    if current_user.is_authenticated:
        subtotal =0
        grandtotal =0 
        customer_id = current_user.id
        get_the_customer = Customer.query.filter_by(id = customer_id).first()

        
        get_the_order = Order.query.filter_by(customer_id = customer_id).order_by(Order.id.desc()).first()
        for key, product in get_the_order.orders.items():
            discount = (product['discount']/100) * int(product['price'])
            subtotal = subtotal + int(product['quantity']) * int(product['price'])
            subtotal = subtotal - discount
            grandtotal = int(subtotal)            



    else:
        return redirect(url_for('customer_login'))
    return render_template('customer/order.html',invoice = invoice, grandtotal = grandtotal, subtotal = subtotal,  get_the_order= get_the_order, get_the_customer = get_the_customer)    



@app.route('/get_pdf/<invoice>', methods =['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        subtotal =0
        grandtotal =0 
        customer_id = current_user.id
        if request.method == "POST":

        
        
            get_the_order = Order.query.filter_by(customer_id = customer_id).first()
            for key, product in get_the_order.orders.items():
                discount = (product['discount']/100) * int(product['price'])
                subtotal = subtotal + int(product['quantity']) * int(product['price'])
                subtotal = subtotal - discount
                grandtotal = int(subtotal)            



   
            result = render_template('customer/pdf.html',invoice = invoice, grandtotal = grandtotal,  get_the_order= get_the_order)    
            pdf = pdfkit.from_string(result, False)
            response = make_response(pdf)
            response.headers['content-Type']='application/pdf'
            response.headers['content-Disposition']= 'inline: filename= output.pdf'
            return response

    return redirect(url_for('order_detail'))





def mergedict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):   
        return dict(list(dict1.items()) + list(dict2.items()))
    return False



@app.route('/addcart', methods =['GET','POST'])
@login_required

def addcart():

    try:
        product_id = request.form.get('product_id')
        quantity =int(request.form.get('quantity'))
        product = Addproduct.query.filter_by(id = product_id).first()
        if request.method == "POST" and product_id and quantity:
            
            # using disctionary 
            items = {product_id:{'name': product.name, 'price': product.price, 'discount': product.discount, 'quantity': quantity, 'stock_1': product.stock, 'image': product.image_1}}
           

            if 'shoppingcart' in session:
                print(session['shoppingcart'])
                if product_id in session['shoppingcart']:
                    for key, item in session['shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                            
                            
                            
                    
                else:
                    session['shoppingcart'] = mergedict( session['shoppingcart'], items)
                    return redirect(request.referrer)

             
            else:
                session['shoppingcart'] = items
                return redirect(request.referrer)


    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
     



@app.route('/carts')
def allcart():
    if 'shoppingcart' not in session:
        return redirect(request.referrer) 
  
    subtotal =0
    grandtotal =0    
    for key , product in session['shoppingcart'].items():
        discount = (product['discount']/100) * int(product['price'])
        subtotal = subtotal + int(product['quantity']) * int(product['price'])
        subtotal = subtotal - discount
        grandtotal = int(subtotal)
    return render_template('products/carts.html', grandtotal = grandtotal, title = 'Cart')    



@app.route('/updatecart/<int:cart_id>', methods=['POST'])
def updatecart(cart_id):
    if 'shoppingcart' not in session or len(session['shoppingcart'])<=0 :
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity') 
        try: 
            session.modified = True
            for key, item in session['shoppingcart'].items():
                if int(key) == cart_id:
                    # if item['stock_1'] < quantity:
                    #     flash(f'Sorry','warning')
                    # else:    
                    item['quantity'] = quantity
                    flash(f'Your cart has been updated','success')
                    return redirect(url_for('allcart'))


        except Exception as e:
            print(e)
            return redirect(url_for('allcart'))   



@app.route('/deletecartitem/<int:id>')
def deletecartitem(id):
    if 'shoppingcart' not in session or len(session['shoppingcart'])<=0 :
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['shoppingcart'].items():
            if int(key)== id:
                session['shoppingcart'].pop(key, None)

                return redirect(url_for('allcart'))
    except Exception as e:
        print(e) 
        return redirect(url_for('allcart'))   


@app.route('/clearcart')
def clearcart():
    try:
        session.pop('shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
    