"""
Saga Orchestrator
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import config
from flask import Flask, jsonify, request
from controllers.order_saga_controller import OrderSagaController

app = Flask(__name__)

@app.get('/health-check')
def health():
    """ Return OK if app is up and running """
    return jsonify({'status': 'ok'})

@app.post('/saga/order')
def saga_order():
    """ Start order saga """
    order_saga_controller = OrderSagaController()
    result = order_saga_controller.run(request)

    if result["status"] == "OK":
        return jsonify(result), 200
    else:
        return jsonify(result), 500

# Start Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.FLASK_PORT)
