from flask import render_template, session, redirect, request, url_for, flash, current_app
from shop import app, db, photos, bcrypt, login_manager
from .forms import CustomerRegistrationForm, CustomerLoginForm
from .models import Customer, Order
from flask_login import login_user, current_user,login_required, logout_user
import secrets, os



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
        
        
        get_the_order = Order.query.filter_by(customer_id = customer_id).first()
        for key, product in get_the_order.orders.items():
            discount = (product['discount']/100) * int(product['price'])
            subtotal = subtotal + int(product['quantity']) * int(product['price'])
            subtotal = subtotal - discount
            grandtotal = int(subtotal)            



    else:
        return redirect(url_for('customer_login'))
    return render_template('customer/order.html',invoice = invoice, grandtotal = grandtotal, subtotal = subtotal,  get_the_order= get_the_order)    
