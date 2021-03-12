from flask import render_template, session, redirect, request, url_for, flash
from shop import app, db
from shop.products.models import Addproduct





def mergedict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):   
        return dict(list(dict1.items()) + list(dict2.items()))
    return False



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
                if product_id in session['shoppingcart']:
                    flash(f"This product is already in your cart", 'info')
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
        discount = (product['discount']/100) * float(product['price'])
        subtotal = subtotal + int(product['quantity']) * float(product['price'])
        subtotal = subtotal - discount
        grandtotal = float(subtotal)
    return render_template('products/carts.html', grandtotal = grandtotal)    
        
# @app.route('/updatecart', methods=['POST'])
# def updatecart
