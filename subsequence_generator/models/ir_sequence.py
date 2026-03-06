from odoo import models, fields, api

class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    has_overlapping_ranges = fields.Boolean(
        string='Has Overlapping Ranges',
        compute='_compute_overlap_status',
        store=False,
        help='Technical field to indicate if this sequence has overlapping date ranges'
    )


    @api.depends('date_range_ids', 'date_range_ids.date_from', 'date_range_ids.date_to')
    def _compute_overlap_status(self):
        for seq in self:
            overlaps = any(r.is_overlapping for r in seq.date_range_ids)
            seq.has_overlapping_ranges = overlaps

class IrSequenceDateRange(models.Model):
    _inherit = 'ir.sequence.date_range'

    is_overlapping = fields.Boolean(
        string='Is Overlapping',
        compute='_compute_is_overlapping',
        store=False
    )


    def _compute_is_overlapping(self):
        for rec in self:
            if not rec.date_from or not rec.date_to:
                rec.is_overlapping = False
                continue
            
            # Check for overlaps within the same sequence
            domain = [
                ('id', '!=', rec.id),
                ('sequence_id', '=', rec.sequence_id.id),
                '|', 
                '|',
                # New Start is between existing Start and End
                '&', ('date_from', '<=', rec.date_from), ('date_to', '>=', rec.date_from),
                # New End is between existing Start and End
                '&', ('date_from', '<=', rec.date_to), ('date_to', '>=', rec.date_to),
                # New range completely covers existing range
                '&', ('date_from', '>=', rec.date_from), ('date_to', '<=', rec.date_to)
            ]
            overlap_count = self.search_count(domain)
            rec.is_overlapping = overlap_count > 0
            rec.is_overlapping = overlap_count > 0