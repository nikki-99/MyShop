from flask import render_template
from shop import app

@app.route('/')
def main():
    return render_template('role.html')