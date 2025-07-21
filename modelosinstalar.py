from odoo import api, fields, models

class GtInstallment(models.Model):
    _name = 'gt.installment'
    _description = 'Parcela de Empréstimo'

    loan_id      = fields.Many2one('gt.loan', 'Empréstimo', required=True, ondelete='cascade')
    number       = fields.Integer('Nº Parcela', required=True)
    due_date     = fields.Date('Vencimento', required=True)
    amount       = fields.Monetary('Valor da Parcela', required=True, currency_field='currency_id')
    paid_amount  = fields.Monetary('Valor Pago', default=0.0, currency_field='currency_id')
    date_payment = fields.Date('Data de Pagamento')
    state        = fields.Selection([
        ('open',    'Pendente'),
        ('paid',    'Pago'),
        ('overdue', 'Atrasada'),
    ], string='Status', compute='_compute_state', store=True)

    currency_id = fields.Many2one('res.currency', string='Moeda',
        default=lambda self: self.env.user.company_id.currency_id)

    @api.depends('paid_amount', 'amount', 'due_date')
    def _compute_state(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.paid_amount >= rec.amount:
                rec.state = 'paid'
            elif rec.due_date < today and rec.paid_amount < rec.amount:
                rec.state = 'overdue'
            else:
                rec.state = 'open'

    @property
    def amount_residual(self):
        return max(self.amount - (self.paid_amount or 0.0), 0.0)
