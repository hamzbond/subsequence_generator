# -*- coding: utf-8 -*-
{
    'name': 'Subsequence Generator for Sequences',
    'version': '1.0.0',
    'category': 'Technical',
    'summary': 'Add subsequence generation and overlapping range detection to sequences',
    'description': """
Generating subsequence date ranges for Odoo sequences manually can be tedious. 
This module allows you to:
- Generate daily, weekly, or monthly subsequences (date ranges) automatically using a wizard.
- Smart numbering: Automatically uses current sequence number for the period containing 'today', and starts from 1 for other periods.
- Detect overlapping date ranges in sequences to avoid numbering conflicts.
- Visual warning indicators for sequences with overlapping ranges.
    """,
    'author': 'hamzbond',
    'website': 'https://hamzbond.github.io',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'wizard/subsequence_generator_wizard_views.xml',
        'views/ir_sequence_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
