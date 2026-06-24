"""
Base controller class
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from abc import abstractmethod
from logger import Logger

class Controller():
    """ Parent controller class. Every saga must have a controller that implements operations. """

    def __init__(self):
        """ Constructor method """
        self.current_saga_state = 0
        self.is_error_occurred = False
        self.logger = Logger.get_instance('Controller')

    @abstractmethod
    def run(self):
        """ Run an operation """
        pass