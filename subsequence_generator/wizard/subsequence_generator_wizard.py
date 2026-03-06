# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime

class IrSequenceSubsequenceWizard(models.TransientModel):
    _name = 'ir.sequence.subsequence.wizard'
    _description = 'Generate Subsequences for Sequence'

    date_start = fields.Date(string='Date Start', required=True, default=fields.Date.context_today)
    date_end = fields.Date(string='Date End', required=True, default=fields.Date.context_today)
    interval = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ], string='Interval', required=True, default='monthly')

    @api.multi
    def action_generate(self):
        self.ensure_one()
        sequence_id = self.env.context.get('active_id')
        if not sequence_id:
            return {'type': 'ir.actions.act_window_close'}
            
        sequence = self.env['ir.sequence'].browse(sequence_id)
        
        # Ensure use_date_range is True
        if not sequence.use_date_range:
            sequence.write({'use_date_range': True})

        d_start = fields.Date.from_string(self.date_start)
        d_end = fields.Date.from_string(self.date_end)

        if d_start > d_end:
            raise UserError(_("Start date cannot be later than end date."))

        current_start = d_start
        today = fields.Date.from_string(fields.Date.context_today(self))
        
        while current_start <= d_end:
            if self.interval == 'daily':
                current_end = current_start
                next_start = current_start + relativedelta(days=1)
            elif self.interval == 'weekly':
                current_end = current_start + relativedelta(days=6)
                if current_end > d_end:
                    current_end = d_end
                next_start = current_start + relativedelta(weeks=1)
            elif self.interval == 'monthly':
                # End of current month
                current_end = current_start + relativedelta(day=31)
                if current_end > d_end:
                    current_end = d_end
                next_start = current_start + relativedelta(months=1, day=1)
            
            # Check if this range already exists
            existing = self.env['ir.sequence.date_range'].search([
                ('sequence_id', '=', sequence.id),
                ('date_from', '=', fields.Date.to_string(current_start)),
                ('date_to', '=', fields.Date.to_string(current_end))
            ])
            
            if not existing:
                # Logic: If range contains today, use current next number, else start from 1
                next_number = 1
                if current_start <= today <= current_end:
                    next_number = sequence.number_next_actual or 1
                
                self.env['ir.sequence.date_range'].create({
                    'sequence_id': sequence.id,
                    'date_from': fields.Date.to_string(current_start),
                    'date_to': fields.Date.to_string(current_end),
                    'number_next_actual': next_number
                })
            
            current_start = next_start
            
        return {'type': 'ir.actions.act_window_close'}
