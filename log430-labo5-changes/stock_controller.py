"""
Product stock controller
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_redis_conn, get_sqlalchemy_session
from flask import jsonify
from stocks.queries.read_stock import get_stock_by_id, get_stock_for_all_products
from stocks.commands.write_stock import populate_redis_from_mysql, set_stock_for_product, update_stock_mysql

def set_stock(request):
    """Set stock quantities of a product"""
    payload = request.get_json() or {}
    product_id = payload.get('product_id')
    quantity = payload.get('quantity')
    try:
        result = set_stock_for_product(product_id, quantity)
        return jsonify({'result': result}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def update_stock(request):
    """Update stock quantities of a product based on given operation (+/-)"""
    payload = request.get_json() or {}
    items = payload.get('items')
    operation = payload.get('operation')
    try:
        session = get_sqlalchemy_session()
        update_stock_mysql(session, items, operation)
        return jsonify({'result': 'OK'}), 201
    except Exception as e:  
        return jsonify({'error': str(e)}), 500

def get_stock(product_id):
    """Get stock quantities of a product"""
    try:
        stock = get_stock_by_id(product_id)
        return jsonify(stock), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def get_stock_overview():
    """Get stock for all products"""
    return get_stock_for_all_products()

def populate_redis_on_startup():
    r = get_redis_conn()
    populate_redis_from_mysql(r)