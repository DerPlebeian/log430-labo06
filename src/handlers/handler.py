"""
Base handler class
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from logger import Logger
from abc import ABC, abstractmethod

class Handler(ABC):
    """ Parent handler class. All child classes must implement run and rollback operations. """

    def __init__(self):
        """ Constructor method """
        self.logger = Logger.get_instance('Handler')

    @abstractmethod
    def run(self):
        """ Run an operation """
        pass

    @abstractmethod
    def rollback(self):
        """ Trigger the rollback of ALL previous operations """
        pass