"""
Titan Islamic AI Core
نواة التطبيق الإسلامي الذكي
"""

__version__ = "4.0.0"
__author__ = "Omar Abdo"
__phone__ = "01289411976"
__email__ = "omar.abdo@titan.com"

from .titan_engine import TitanEngine
from .database import IslamicDatabase
from .config import AppConfig

__all__ = ['TitanEngine', 'IslamicDatabase', 'AppConfig']
