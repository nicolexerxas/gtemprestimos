# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import timedelta
import calendar

class GtLoan(models.Model):
    _name = 'gt.loan'
    _description = 'Empréstimo GT'
    _inherit = ['mail.thread']

    name               = fields.Char('Número', readonly=True, default='NEW', tracking=True)
    partner_id         = fields.Many2one('res.partner', 'Cliente', required=True, tracking=True)
    valor_solicitado   = fields.Monetary('Valor Solicitado', required=True, currency_field='currency_id', tracking=True)
    valor_liberado     = fields.Monetary('Valor Liberado', currency_field='currency_id', tracking=True)
    taxa_juros         = fields.Float('Juros (%) por Semana', required=True, digits=(12,2), tracking=True)
    prazo_semanas      = fields.Integer('Prazo (semanas)', required=True, tracking=True)
    data_inicio        = fields.Date('Data de Início', default=fields.Date.context_today, tracking=True)
    state              = fields.Selection([
                            ('draft', 'Aguardando'),
                            ('active','Ativo'),
                            ('paid',  'Quitado'),
                            ('bad',   'Inadimplente'),
                        ], string='Status', default='draft', tracking=True)

    installment_ids    = fields.One2many('gt.installment', 'loan_id', 'Parcelas', readonly=True)
    renegotiation_ids  = fields.One2many('gt.loan.reneg', 'loan_id', 'Renegociações')
    currency_id        = fields.Many2one('res.currency','Moeda', readonly=True,
                            default=lambda self: self.env.user.company_id.currency_id)

    @api.model
    def create(self, vals):
        if vals.get('name','NEW') == 'NEW':
            vals['name'] = self.env['ir.sequence'].next_by_code('gt.loan') or 'NEW'
        return super().create(vals)

    def action_approve(self):
        self.ensure_one()
        self._apply_debt_discount()
        self.valor_liberado = self.valor_solicitado
        self.state = 'active'
        self._generate_installments()

    def _apply_debt_discount(self):
        for loan in self:
            pendentes = self.env['gt.installment'].search([
                ('loan_id.partner_id','=', loan.partner_id.id),
                ('state','in',['open','overdue'])
            ])
            total_debito = sum(p.amount - (p.paid_amount or 0) for p in pendentes)
            if total_debito > 0:
                loan.valor_liberado = max(loan.valor_solicitado - total_debito, 0)
                for parc in pendentes:
                    parc.write({
                        'paid_amount': parc.amount,
                        'date_payment': fields.Date.context_today(loan),
                    })
                loan.message_post(body=f'Descontados R${total_debito:.2f} de dívidas anteriores.')

    def _generate_installments(self):
        self.ensure_one()
        self.installment_ids.unlink()
        principal = self.valor_liberado
        weeks     = self.prazo_semanas
        rate      = self.taxa_juros / 100.0
        total_int = principal * rate * weeks
        total     = principal + total_int
        value_each= total / weeks
        start     = fields.Date.from_string(self.data_inicio)
        for i in range(1, weeks+1):
            due = start + timedelta(days=7*i)
            while calendar.weekday(due.year, due.month, due.day) in (5,6):
                due += timedelta(days=1)
            self.env['gt.installment'].create({
                'loan_id':    self.id,
                'number':     i,
                'due_date':   due,
                'amount':     value_each,
            })
