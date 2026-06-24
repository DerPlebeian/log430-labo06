"""
Load configurations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import os
from dotenv import load_dotenv

load_dotenv()

FLASK_PORT = int(os.getenv("FLASK_PORT"))
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")
