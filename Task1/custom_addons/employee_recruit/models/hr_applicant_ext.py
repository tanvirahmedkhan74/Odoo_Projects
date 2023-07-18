from odoo import models, fields


class ApplicantExtension(models.Model):
    _inherit = 'hr.applicant'

    emergency_ids = fields.One2many('hr.employee', 'emergency_id', string="emergency")
    education_ids = fields.One2many('hr.employee', 'education_id', string="education")


class ApplicantEmployeeExt(models.Model):
    _inherit = 'hr.employee'

    emergency_id = fields.Many2one('hr.applicant', string="Emergency")
    education_id = fields.Many2one('hr.applicant', string="Education")

    emp_name = fields.Char('Name')
    emp_phone = fields.Char('Phone')
    emp_address = fields.Char('Address')

    institute = fields.Char('Institute')
    degree = fields.Char('Degree')
    passing_year = fields.Char('Passing Year')
