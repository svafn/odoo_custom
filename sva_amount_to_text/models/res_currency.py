# -*- coding: utf-8 -*-

import logging
from odoo import models, tools

try:
    from num2words import num2words
except ImportError:
    num2words = None

_logger = logging.getLogger(__name__)


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    def amount_to_text(self, amount):
        """
        Переопределена версія методу amount_to_text із використанням num2words
        з параметрами to='currency' для правильної граматики та розділювачів
        """
        self.ensure_one()
        
        if num2words is None:
            _logger.warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""
        
        lang = tools.get_lang(self.env)
        
        try:
            # Використовуємо num2words з параметрами to='currency' та currency
            # Це автоматично піклується про граматику та розділювачі
            result = num2words(amount, lang=lang.iso_code, to='currency', currency=self.name)
            # Робимо першу букву великою
            return result.capitalize()
        except (NotImplementedError, KeyError, TypeError):
            # Якщо currency не підтримується для цієї мови, спробуємо англійську
            try:
                result = num2words(amount, lang='en', to='currency', currency=self.name)
                return result.capitalize()
            except Exception as e:
                _logger.warning(f"Error converting amount to text: {e}")
                # Останній fallback - просто число без валюти
                return str(amount)
