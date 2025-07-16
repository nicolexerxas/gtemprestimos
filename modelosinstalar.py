from odoo import fields, models

class GtInstallment(models.Model):
    _name = 'gt.installment'
    _description = 'Parcela de Empréstimo'

    loan_id = fields.Many2one('gt.loan', 'Empréstimo', required=True, ondelete='cascade')
    number  = fields.Integer('Nº Parcela', required=True)
    due_date = fields.Date('Vencimento', required=True)
    amount   = fields.Monetary('Valor da Parcela', required=True, currency_field='currency_id')
    paid_amount = fields.Monetary('Valor Pago', default=0.0, currency_field='currency_id')
    date_payment = fields.Date('Data de Pagamento')
    state = fields.Selection([
        ('open',    'Pendente'),
        ('paid',    'Pago'),
        ('overdue', 'Atrasada'),
    ], default='open')

    @property
    def amount_residual(self):
        return max(self.amount - (self.paid_amount or 0.0), 0.0)