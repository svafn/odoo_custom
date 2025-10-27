from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def preview_invoice(self):
        """Override to open invoice preview in new tab"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.get_portal_url(),
            'target': 'new',  # Ось ключова зміна!
        }
