"""
Handler: delete order
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import config
import requests
from handlers.handler import Handler
from order_saga_state import OrderSagaState

class DeleteOrderHandler(Handler):
    """ Handle order deletion. """

    def __init__(self, order_id):
        """ Constructor method """
        self.order_id = order_id
        super().__init__()

    def run(self):
        """Call StoreManager to check out from stock"""
        try:
            response = requests.delete(
                f'{config.API_GATEWAY_URL}/store-manager-api/orders/{self.order_id}',
                headers={'Content-Type': 'application/json'}
            )

            if response.ok:
                self.logger.debug("Transition d'état: DeleteOrder -> ORDER_DELETED")
                return OrderSagaState.ORDER_DELETED

            try:
                payload = response.json()
            except Exception:
                payload = response.text
            self.logger.error(f"DeleteOrder a échoué : {response.status_code} - {payload}")
            return OrderSagaState.END

        except Exception as e:
            self.logger.error("DeleteOrder a échoué : " + str(e))
            return OrderSagaState.END
        
    def rollback(self):
        """
        (rollback not applicable for DeleteOrder)
        """
        # Nous héritons de la classe abstraite Handler, et par conséquent, l'implémentation de la méthode rollback() est obligatoire.
        pass
