from odoo import models, fields, api

class CurrencyExchange(models.Model):
    _name = 'currency.exchange'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'reference'
    _description = 'Currency Exchange'

    date = fields.Date(default=fields.Date.today, string="Date")
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: ('New'))
    partner_id = fields.Many2one('res.partner', string='Customer')
    currency_from_id = fields.Many2one('res.currency', string="Currency From", required=True)
    currency_to_id = fields.Many2one('res.currency', string="Currency To", required=True)
    amount_given = fields.Monetary(string="Amount Given", currency_field='currency_from_id', required=True)
    exchanged_amount = fields.Monetary(string="Exchanged Amount", currency_field='currency_to_id',
                                       compute='_compute_amount_received', store=True)
    journal_id = fields.Many2one('account.journal',
                                 string="Journal",
                                 default=lambda self: self.env['account.journal'].search([('name', '=', 'Exchange Difference')],))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
    ], default='draft', string="Status")
    service_fee = fields.Monetary(string="Service Fee",
                                  currency_field='currency_from_id',
                                  compute='compute_service_amount',
                                  store=True,
                                  default=0.0,
                                  required=True)
    total_amount_received = fields.Monetary(string="Amount Payable", currency_field='currency_to_id')

    @api.model
    def create(self, vals):
        if vals.get('reference', ('New')) == ('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('currency.exchange') or ('New')
        res = super(CurrencyExchange, self).create(vals)
        return res

    @api.depends('amount_given', 'currency_from_id', 'currency_to_id', 'date')
    def _compute_amount_received(self):
        for record in self:
            if record.currency_from_id and record.currency_to_id and record.amount_given:
                record.exchanged_amount = record.currency_from_id._convert(
                    record.amount_given,
                    record.currency_to_id,
                    self.env.company,
                    record.date
                )
            else:
                record.exchanged_amount = 0

    @api.depends('exchanged_amount','total_amount_received','service_fee')
    def compute_service_amount(self):
        for record in self:
            if record.exchanged_amount and record.total_amount_received:
                record.service_fee = (record.exchanged_amount - record.total_amount_received)

    def action_create_journal_entry(self):
        """Create journal entry for currency exchange fee"""
        for record in self:
            if record.service_fee:
                move = self.env['account.move'].create({
                    'journal_id': record.journal_id.id,
                    'date': record.date,
                    'partner_id': record.partner_id.id,
                    'ref': record.reference,
                    'line_ids': [
                        (0, 0, {
                            'account_id': record.journal_id.id,
                            'currency_id': record.currency_to_id.id,
                            'partner_id': record.partner_id.id,
                            'credit': record.service_fee,
                            'name': 'Currency Exchange Fee',
                        }),
                        (0, 0, {
                            'account_id': record.journal_id.id,
                            'currency_id': record.currency_to_id.id,
                            'partner_id': record.partner_id.id,
                            'debit': record.service_fee,
                            'name': 'Currency Exchange Fee',
                        })
                    ]
                })
                move.action_post()
                record.state = 'posted'

    def action_view_journal(self):
        journal = self.env['account.move'].search([('ref', '=', self.reference)], limit=1)
        if journal:
            return {
                'name': 'Journal',
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': journal.id,
            }
        else:
            return {'type': 'ir.actions.act_window_close'}

