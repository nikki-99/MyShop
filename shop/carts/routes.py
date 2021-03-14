from flask import render_template, session, redirect, request, url_for, flash
from shop import app, db
from shop.products.models import Addproduct
from shop.products.routes import brands, categories




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
    return render_template('products/carts.html', grandtotal = grandtotal, title = 'Cart', brands = brands(), categories = categories())    



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


