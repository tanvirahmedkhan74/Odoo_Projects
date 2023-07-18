# from odoo import fields, models, api
#
#
# class HrEmployee(models.Model):
#     _inherit = 'hr.employee'
#
#     emergency_id = fields.One2many('hr.employee.emergency', 'emp_id', string="Emergency Contact")
#     # manager = fields.Many2one(string="Manager Name", selection='_get_manager_ids')
#
#     def _get_manager_ids(self):
#         managers = self.env['hr.department'].search([('manager_id', '>=', 0), ('active', '=', True)])
#
#         return [(x.id, x.name) for x in managers]
#
#
# class Emergency(models.Model):
#     _name = 'hr.employee.emergency'
#
#     emp_id = fields.Many2one('hr.employee', string="Emp")
#
#     em_name = fields.Char('Name')
#     em_phone = fields.Char('Phone')
#     em_address = fields.Char('Address')
