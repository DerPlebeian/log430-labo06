"""
Handler: create payment transaction
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import config
import requests
from handlers.handler import Handler
from order_saga_state import OrderSagaState

class CreatePaymentHandler(Handler):
    """ Handle the creation of a payment transaction for a given order. Trigger rollback of previous steps in case of failure. """

    def __init__(self, order_id, order_data):
        """ Constructor method """
        self.order_id = order_id
        self.order_data = order_data
        self.total_amount = 0
        super().__init__()

    def run(self):
        """Call payment microservice to generate payment transaction"""
        try:
            response_order = requests.get(
                f'{config.API_GATEWAY_URL}/store-manager-api/orders/{self.order_id}',
                headers={'Content-Type': 'application/json'}
            )

            if not response_order.ok:
                try:
                    payload = response_order.json()
                except Exception:
                    payload = response_order.text
                self.logger.error(f"CreatePayment a échoué lors de la lecture de la commande : {response_order.status_code} - {payload}")
                return self.rollback()

            order_payload = response_order.json() or {}
            self.total_amount = order_payload.get('total_amount')
            if self.total_amount is None and isinstance(order_payload.get('order'), dict):
                self.total_amount = order_payload['order'].get('total_amount')

            if self.total_amount is None:
                self.logger.error(f"CreatePayment a échoué : total_amount introuvable pour la commande {self.order_id}")
                return self.rollback()

            response_payment = requests.post(
                f'{config.API_GATEWAY_URL}/payments-api/payments',
                json={
                    'order_id': self.order_id,
                    'user_id': self.order_data.get('user_id'),
                    'total_amount': self.total_amount
                },
                headers={'Content-Type': 'application/json'}
            )

            if response_payment.ok:
                self.logger.debug("Transition d'état: CreatePayment -> PAYMENT_CREATED")
                return OrderSagaState.PAYMENT_CREATED

            try:
                payload = response_payment.json()
            except Exception:
                payload = response_payment.text
            self.logger.error(f"CreatePayment a échoué lors de la création du paiement : {response_payment.status_code} - {payload}")
            return self.rollback()

        except Exception as e:
            self.logger.error("CreatePayment a échoué : " + str(e))
            return self.rollback()
        
    def rollback(self):
        """ Call StoreManager to restore stock quantities if payment transaction creation fails """
        try:
            response = requests.put(
                f'{config.API_GATEWAY_URL}/store-manager-api/stocks',
                json={
                    'items': self.order_data.get('items', []),
                    'operation': '+'
                },
                headers={'Content-Type': 'application/json'}
            )

            if response.ok:
                self.logger.debug("Transition d'état: CreatePaymentFailure -> STOCK_INCREASED")
                return OrderSagaState.STOCK_INCREASED

            try:
                payload = response.json()
            except Exception:
                payload = response.text
            self.logger.error(f"Rollback CreatePayment a échoué : {response.status_code} - {payload}")
            return OrderSagaState.END

        except Exception as e:
            self.logger.error("Rollback CreatePayment a échoué : " + str(e))
            return OrderSagaState.END