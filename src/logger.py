"""
Logger
SPDX-License-Identifier: LGPL-3.0-or-later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import logging
import sys

class Logger:
    """ This class logs messages to the terminal """
    
    @staticmethod
    def get_instance(name: str, level=logging.DEBUG, log_to_file=False):
        """ Set up a logger to stdout. Works for both the Docker terminal and the host machine terminal """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False
        
        # Prevent duplicate handlers if logger already exists
        if logger.handlers:
            return logger
        
        # Format of the string that will be logged
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (.log file, optional)
        if (log_to_file):
            fileHandler = logging.FileHandler("sensors_visualization.log")
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
        
        # Ensure root logger doesn't interfere
        logging.root.setLevel(logging.WARNING)
        
        return logger