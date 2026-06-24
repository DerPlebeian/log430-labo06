"""
Handler: create order
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import config
import requests
from handlers.handler import Handler
from order_saga_state import OrderSagaState

class CreateOrderHandler(Handler):
    """ Handle order creation. """

    def __init__(self, order_data):
        """ Constructor method """
        self.order_data = order_data
        self.order_id = 0
        super().__init__()

    def run(self):
        """Call StoreManager to create order"""
        try:
            # ATTENTION: Si vous exécutez ce code dans Docker, n'utilisez pas localhost. Utilisez plutôt le hostname de votre API Gateway
            response = requests.post(f'{config.API_GATEWAY_URL}/store-manager-api/orders',
                json=self.order_data,
                headers={'Content-Type': 'application/json'}
            )
            if response.ok:
                data = response.json() 
                self.order_id = data['order_id'] if data else 0
                self.logger.debug("Transition d'état: CreateOrder -> ORDER_CREATED")
                return OrderSagaState.ORDER_CREATED
            else:
                text = response.json() 
                self.logger.error(f"CreateOrder a échoué : {response.status_code} - {text}")
                return OrderSagaState.END

        except Exception as e:
            self.logger.error("CreateOrder a échoué : " + str(e))
            return OrderSagaState.END
        
    def rollback(self):
        """
        (rollback not applicable for CreateOrder)
        """
        # Une compensation n'est pas nécessaire car la commande n'a pas été créée. Il n'y a donc rien à compenser. 
        # Cependant, nous héritons de la classe abstraite Handler, et par conséquent, l'implémentation de la méthode rollback() est obligatoire.
        pass