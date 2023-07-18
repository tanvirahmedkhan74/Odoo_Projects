from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    education_id = fields.One2many('hr.employee.education', 'emp_id', string="Education")


class HrEducation(models.Model):
    _name = 'hr.employee.education'

    emp_id = fields.Many2one('hr.employee', 'Employee ID')
    institute = fields.Char('Institute')
    degree = fields.Char('Degree')
    passing_year = fields.Char('Passing Year')
