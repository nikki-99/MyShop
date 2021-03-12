from flask import render_template, session, redirect, request, url_for, flash
from shop import app, db
from shop.products.models import Addproduct



@app.route('/addcart', methods =['GET','POST'])
def addcart():
    try:
        product_id = request.form.get('product_id')
        quantity =request.form.get('quantity')
        product = Addproduct.query.filter_by(id = product_id).first()
        if request.method == "POST" and product_id and quantity:
            # using disctionary 
            items = {product_id:{'name': product.name, 'price': product.price, 'discount': product.discount, 'quantity': quantity, 'image': product.image_1}}
             

            if 'shoppingcart' in session:
                print(session['shoppingcart'])
             
            else:
                session['shoppingcart'] = items
                return redirect(request.referrer)


    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

