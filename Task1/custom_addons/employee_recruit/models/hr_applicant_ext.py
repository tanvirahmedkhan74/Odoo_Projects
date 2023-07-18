from odoo import models, fields


class ApplicantExtension(models.Model):
    _inherit = 'hr.applicant'

    emergency_ids = fields.One2many('hr.applicant.emg', 'emergency_id', string="||")
    education_ids = fields.One2many('hr.applicant.edu', 'education_id', string="||")


class ApplicantEmployeeEmergency(models.Model):
    _name = 'hr.applicant.emg'

    emergency_id = fields.Many2one('hr.applicant', string="Emergency")

    emp_name = fields.Char('Name')
    emp_phone = fields.Char('Phone')
    emp_address = fields.Char('Address')


class ApplicationEmployeeEducation(models.Model):
    _name = 'hr.applicant.edu'

    education_id = fields.Many2one('hr.applicant', string="Education")
    # employee_edu = fields.Many2one('hr.employee', string="Education")

    institute = fields.Char('Institute')
    degree = fields.Char('Degree')
    passing_year = fields.Char('Passing Year')
